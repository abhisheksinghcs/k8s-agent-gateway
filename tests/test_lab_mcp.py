# Local contract tests: loopback upstream stubs -> real SDK HTTP -> offline
# configuration/packaging checks. No GPU, cluster, downloads or client scaffold.
import asyncio
import configparser
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import logging
from pathlib import Path
import socket
import threading
import time
import tomllib
from urllib.parse import urlsplit

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import pytest
import uvicorn
import yaml

import main


SENTINEL = "DO_NOT_LEAK_SENTINEL_SECRET"


@pytest.fixture(autouse=True)
def safe_logs():
    # Capture only application outcomes; hostile dependency diagnostics stay off.
    main.configure_logging()
    output = io.StringIO()
    main.APP_LOG.handlers = [logging.StreamHandler(output)]
    yield output


@contextmanager
def upstream(status=200, body=b'{"status":"ok"}', delay=0, headers=None, chunk_delay=0):
    # Record the one permitted GET and emulate bounded upstream failure modes.
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requests.append((self.command, self.path))
            time.sleep(delay)
            self.send_response(status)
            for name, value in (headers or {}).items():
                self.send_header(name, value)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                if chunk_delay:
                    for value in body:
                        self.wfile.write(bytes([value]))
                        self.wfile.flush()
                        time.sleep(chunk_delay)
                else:
                    self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def log_message(self, format, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/health", requests
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)
        assert not worker.is_alive()


@contextmanager
def running_app(upstream_url="http://127.0.0.1:1/health"):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
        app = main.create_app(
            upstream=upstream_url,
            allowed_hosts=[f"127.0.0.1:{port}", "lab-info.mcp.svc.cluster.local:80"],
            allowed_origins=[f"http://127.0.0.1:{port}", "http://lab-info.mcp.svc.cluster.local"],
        )
        server = uvicorn.Server(uvicorn.Config(
            app, host="127.0.0.1", port=port, log_config=None, access_log=False,
            proxy_headers=False, timeout_graceful_shutdown=2,
        ))
        worker = threading.Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        worker.start()
        try:
            deadline = time.monotonic() + 5
            while not server.started:
                assert worker.is_alive() and time.monotonic() < deadline
                time.sleep(0.01)
            yield f"http://127.0.0.1:{port}"
        finally:
            server.should_exit = True
            worker.join(timeout=5)
            assert not worker.is_alive()


async def exercise_sdk(url):
    # Initialization/discovery/both calls prove MCP behavior, not merely HTTP 200.
    async with httpx.AsyncClient(trust_env=False) as client:
        async with streamable_http_client(f"{url}/mcp", http_client=client) as (read, write, session_id):
            async with ClientSession(read, write) as session:
                initialized = await session.initialize()
                assert initialized.protocolVersion == "2025-11-25"
                tools = (await session.list_tools()).tools
                assert {tool.name for tool in tools} == {"get_lab_overview", "get_model_health"}
                results = {}
                for tool in tools:
                    assert tool.inputSchema.get("properties", {}) == {}
                    assert tool.outputSchema
                    assert tool.annotations.readOnlyHint
                    result = await session.call_tool(tool.name, {})
                    assert not result.isError
                    assert result.structuredContent
                    results[tool.name] = result.structuredContent
                assert session_id() is None
                overview = results["get_lab_overview"]
                assert set(overview) == {"purpose", "components", "intended_request_path", "limitations", "models"}
                assert len(overview["models"]) == 4
                return results["get_model_health"]


def rpc(url, method="tools/call", params=None, headers=None):
    return httpx.post(
        f"{url}/mcp", trust_env=False,
        headers={
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2025-11-25", **(headers or {}),
        },
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}},
    )


def test_config_and_application():
    assert len(main.load_overview(Path("config/lab-info.json"))["models"]) == 4
    assert main.create_app()


@pytest.mark.parametrize("body", [b"not-json", b"[]", b"{}", b'{"overview":null}'])
def test_invalid_config_fails_before_serving(body, monkeypatch):
    # Invalid configuration must fail at assembly, not on the first tool call.
    monkeypatch.setattr(Path, "read_bytes", lambda path: body)
    with pytest.raises(ValueError, match="^Invalid lab configuration$"):
        main.create_app()


@pytest.mark.parametrize("hosts,origins", [([], []), (["*"], []), (["localhost:8000"], ["*"])])
def test_wildcard_or_missing_authority_is_rejected(hosts, origins):
    with pytest.raises(ValueError, match="^Invalid transport configuration$"):
        main.create_app(allowed_hosts=hosts, allowed_origins=origins)


@pytest.mark.parametrize("host,port", [(None, None), ("0.0.0.0", "8123")])
def test_main_listener_contract(host, port, monkeypatch):
    # Inspect Uvicorn wiring without opening sockets; pod binding is explicit.
    for name in ("LAB_HOST", "LAB_PORT", "LAB_CONFIG", "LAB_HEALTH_URL",
                 "LAB_ALLOWED_HOSTS", "LAB_ALLOWED_ORIGINS"):
        monkeypatch.delenv(name, raising=False)
    if host is not None:
        monkeypatch.setenv("LAB_HOST", host)
        monkeypatch.setenv("LAB_PORT", port)
    calls = []
    monkeypatch.setattr(main.uvicorn, "run", lambda app, **options: calls.append(options))
    main.main()
    assert calls == [{"host": host or "127.0.0.1", "port": int(port or 8000),
                      "access_log": False, "log_config": None, "proxy_headers": False}]


@pytest.mark.parametrize("failure", ["listener", "upstream", "file"])
def test_startup_error_does_not_echo_configuration(failure, monkeypatch, safe_logs, capfd):
    # Operator mistakes are constant startup failures, never exception/URL dumps.
    monkeypatch.setattr(main, "configure_logging", lambda: None)
    if failure == "listener":
        monkeypatch.setenv("LAB_PORT", SENTINEL)
    elif failure == "upstream":
        monkeypatch.setenv("LAB_HEALTH_URL", "http://user:" + SENTINEL + "@localhost/health")
    else:
        monkeypatch.setenv("LAB_CONFIG", SENTINEL)
    with pytest.raises(SystemExit) as stopped:
        main.main()
    assert stopped.value.code == 1
    assert safe_logs.getvalue().strip() == "startup_failed invalid_configuration"
    captured = capfd.readouterr()
    assert SENTINEL not in captured.out + captured.err


@pytest.mark.parametrize("url", [
    "file:///health", "http://user:secret@localhost/health", "http://localhost/models",
    "http://localhost/health?url=secret", "http://localhost/health#secret",
    "http://localhost:0/health", "http://localhost:65536/health",
    "http://localhost:bad/health", "http://localhost/health?", "http://localhost/health#",
    "http://localhost/health\n", "http:///health",
])
def test_reject_health_url(url):
    with pytest.raises(ValueError):
        main.health_url(url)


def test_connection_failure_is_safe():
    result = asyncio.run(main.observe_health("http://127.0.0.1:1/health"))
    assert result == {"status": "unknown", "reason": "connection_failed", "http_status": None}


def test_sdk_http_initialize_discover_and_all_calls(safe_logs):
    with upstream() as (target, requests), running_app(target) as url:
        result = asyncio.run(exercise_sdk(url))
        assert result["status"] == "healthy"
        assert set(result) == {"status", "reason", "http_status"}
        assert requests == [("GET", "/health")]
    assert {"startup", "shutdown", "get_lab_overview ok", "get_model_health health_ok"} <= set(safe_logs.getvalue().splitlines())


@pytest.mark.parametrize("status,body,expected,reason", [
    (200, b'{"status":"ok"}', "healthy", "health_ok"),
    (200, ('{"status":"ok","extra":"' + SENTINEL + '"}').encode(), "healthy", "health_ok"),
    (503, b'{"status":"loading model"}', "loading", "model_loading"),
    (503, b'{"status":"ok"}', "unknown", "invalid_response"),
    (503, b'{}', "unknown", "invalid_response"),
    (503, SENTINEL.encode(), "unknown", "invalid_response"),
    (404, SENTINEL.encode(), "unhealthy", "http_error"),
    (500, SENTINEL.encode(), "unhealthy", "http_error"),
    (200, SENTINEL.encode(), "unknown", "invalid_response"),
    (200, b'{"status":"secret"}', "unknown", "invalid_response"),
    (200, b'{"status":"loading model"}', "unknown", "invalid_response"),
    (200, b'[]', "unknown", "invalid_response"),
    (200, b'{"status":true}', "unknown", "invalid_response"),
    (204, b'', "unknown", "invalid_response"),
    (200, b"x" * (main.HEALTH_LIMIT + 1), "unknown", "response_too_large"),
    (302, b"", "unknown", "redirect_rejected"),
])
def test_upstream_cases(status, body, expected, reason, safe_logs, monkeypatch):
    monkeypatch.setenv("HTTP_PROXY", f"http://{SENTINEL}.invalid:1")
    monkeypatch.setenv("HTTPS_PROXY", f"http://{SENTINEL}.invalid:1")
    monkeypatch.setenv("ALL_PROXY", f"http://{SENTINEL}.invalid:1")
    with upstream(status, body, headers={"Location": f"http://{SENTINEL}.invalid/inference"}) as (target, requests):
        result = asyncio.run(main.observe_health(target))
        assert result == {"status": expected, "reason": reason, "http_status": status}
        assert requests == [("GET", "/health")]
        assert SENTINEL not in json.dumps(result)
        assert SENTINEL not in safe_logs.getvalue()


def test_timeout(monkeypatch):
    monkeypatch.setattr(main, "HEALTH_TIMEOUT", 0.05)
    with upstream(delay=0.2) as (target, requests):
        result = asyncio.run(main.observe_health(target))
        assert result["reason"] == "timeout"
        assert requests == [("GET", "/health")]


def test_overall_deadline_bounds_slow_body(monkeypatch):
    assert main.HEALTH_TIMEOUT == 3.0
    monkeypatch.setattr(main, "HEALTH_TIMEOUT", 0.08)
    with upstream(chunk_delay=0.02) as (target, requests):
        started = time.monotonic()
        result = asyncio.run(main.observe_health(target))
        assert result["reason"] == "timeout"
        assert time.monotonic() - started < 0.5
        assert result["http_status"] == 200
        assert requests == [("GET", "/health")]


def test_dns_failure(monkeypatch):
    def fail_dns(*args, **kwargs):
        raise socket.gaierror(SENTINEL)

    monkeypatch.setattr(socket, "getaddrinfo", fail_dns)
    result = asyncio.run(main.observe_health("http://unresolvable.invalid/health"))
    assert result["reason"] == "connection_failed"
    assert SENTINEL not in json.dumps(result)


def test_upstream_failure_does_not_break_mcp_or_probes(monkeypatch):
    # Only the live tool may call observe_health; overview/probes are independent.
    original = main.observe_health
    calls = []

    async def observed(target):
        calls.append(target)
        return await original(target)

    monkeypatch.setattr(main, "observe_health", observed)
    with running_app() as url:
        result = asyncio.run(exercise_sdk(url))
        assert result["reason"] == "connection_failed"
        for path in ("/healthz", "/readyz"):
            assert httpx.get(url + path, trust_env=False).json() == {"status": "ok"}
    assert calls == ["http://127.0.0.1:1/health"]


def test_extra_arguments_cannot_change_target_or_action(safe_logs, capfd):
    # SDK ignores extra keys for these handlers; this is NOT strict rejection.
    with upstream() as (target, requests), running_app(target) as url:
        for name, arguments in [
            ("get_model_health", {"url": SENTINEL}),
            ("get_lab_overview", {"path": SENTINEL}),
        ]:
            response = rpc(url, params={"name": name, "arguments": arguments}, headers={"Authorization": SENTINEL})
            assert not response.json()["result"].get("isError", False)
            assert SENTINEL not in response.text
        response = rpc(url, params={"name": "not_a_registered_tool", "arguments": {"url": SENTINEL}})
        assert response.json()["result"]["isError"]
        assert SENTINEL not in response.text
        assert requests == [("GET", "/health")]
    assert SENTINEL not in safe_logs.getvalue()
    captured = capfd.readouterr()
    assert SENTINEL not in captured.out + captured.err


def test_transport_security_on_mcp_and_probes(safe_logs, capfd):
    # Custom routes use the same SDK validator explicitly, including bad Origins.
    with running_app() as url:
        for header, value, expected in [
            ("Host", SENTINEL, 421), ("Origin", f"https://{SENTINEL}.invalid", 403),
        ]:
            for path in ("/mcp", "/healthz", "/readyz"):
                response = (rpc(url, headers={header: value}) if path == "/mcp" else
                            httpx.get(url + path, headers={header: value}, trust_env=False))
                assert response.status_code == expected
                assert SENTINEL not in response.text
        response = rpc(url, "tools/list", headers={"Host": "lab-info.mcp.svc.cluster.local:80", "Origin": "http://lab-info.mcp.svc.cluster.local"})
        assert len(response.json()["result"]["tools"]) == 2
    assert SENTINEL not in safe_logs.getvalue()
    captured = capfd.readouterr()
    assert SENTINEL not in captured.out + captured.err


def test_application_error_redaction(safe_logs, monkeypatch, capfd):
    # App failures have constant ToolError output; SDK envelope errors do not.
    with running_app() as url:
        async def failure(*args):
            raise RuntimeError(SENTINEL)

        monkeypatch.setattr(main, "observe_health", failure)
        response = rpc(url, params={"name": "get_model_health"})
        assert response.json()["result"]["isError"]
        assert "Tool execution failed" in response.text
        assert SENTINEL not in response.text
    assert SENTINEL not in safe_logs.getvalue()
    captured = capfd.readouterr()
    assert SENTINEL not in captured.out + captured.err


@pytest.mark.parametrize("case", ["envelope", "protocol", "unknown_tool"])
def test_sdk_reflection_characterization(case, safe_logs, capfd):
    # MEDIUM accepted residual: SDK responses can reflect caller-controlled data.
    # This deliberately contradicts the removed guard's redaction guarantee.
    with running_app() as url:
        if case == "envelope":
            response = httpx.post(url + "/mcp", trust_env=False,
                json={"jsonrpc": SENTINEL, "id": 1, "method": "tools/list"},
                headers={"Accept": "application/json"})
            assert response.status_code == 400
        elif case == "protocol":
            response = rpc(url, "tools/list", headers={"MCP-Protocol-Version": SENTINEL})
            assert response.status_code == 400
        else:
            response = rpc(url, params={"name": SENTINEL})
            assert response.json()["result"]["isError"]
        assert SENTINEL in response.text
    assert SENTINEL not in safe_logs.getvalue()
    captured = capfd.readouterr()
    assert SENTINEL not in captured.out + captured.err


@pytest.mark.parametrize("size,chunked,expected", [
    (65536, False, 200), (65537, False, 413), (65537, True, 413),
])
def test_mcp_body_limit(size, chunked, expected, safe_logs):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}).encode()
    body += b" " * (size - len(body))
    content = iter([body[:32768], body[32768:]]) if chunked else body
    with running_app() as url:
        response = httpx.post(
            url + "/mcp", content=content, trust_env=False,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        assert response.status_code == expected
        if expected == 200:
            assert len(response.json()["result"]["tools"]) == 2
    assert SENTINEL not in safe_logs.getvalue()


@pytest.mark.parametrize("headers,expected", [
    ({"Accept": "text/plain", "Content-Type": "application/json"}, 406),
    ({"Accept": "application/json", "Content-Type": "text/plain"}, 400),
    ({"Accept": "application/json", "Content-Type": "application/json-invalid"}, 415),
])
def test_malformed_body_preserves_header_errors(headers, expected, safe_logs, capfd):
    with running_app() as url:
        response = httpx.post(url + "/mcp", content=SENTINEL, headers=headers, trust_env=False)
        assert response.status_code == expected
        assert SENTINEL not in response.text
    assert SENTINEL not in safe_logs.getvalue()
    captured = capfd.readouterr()
    assert SENTINEL not in captured.out + captured.err


def test_reject_compressed_response():
    with upstream(body=b"not-decoded", headers={"Content-Encoding": "gzip"}) as (target, requests):
        result = asyncio.run(main.observe_health(target))
        assert result["reason"] == "unexpected_encoding"
        assert requests == [("GET", "/health")]


def test_curated_and_packaged_config_drift():
    config = json.loads(Path("config/lab-info.json").read_text())
    manifest = list(yaml.safe_load_all(Path("k8s/mcp/lab-info.yaml").read_text()))
    packaged = next(item for item in manifest if item["kind"] == "ConfigMap")
    assert json.loads(packaged["data"]["lab-info.json"]) == config
    source = list(yaml.safe_load_all(Path("k8s/llm/llama-cpp.yaml").read_text()))
    preset_map = next(item for item in source if item["kind"] == "ConfigMap")
    parser = configparser.ConfigParser()
    parser.read_string("[DEFAULT]\n" + preset_map["data"]["models.ini"])
    expected = {name: parser[name]["hf-repo"] for name in parser.sections()}
    assert {item["id"]: f'{item["repository"]}:{item["quantization"]}' for item in config["presets"]["models"]} == expected


def test_manifest_security_and_service_allowlists():
    manifest = list(yaml.safe_load_all(Path("k8s/mcp/lab-info.yaml").read_text()))
    assert {item["kind"] for item in manifest} == {"Namespace", "ConfigMap", "Deployment", "Service"}
    deployment = next(item for item in manifest if item["kind"] == "Deployment")
    assert deployment["spec"]["replicas"] == 1
    pod = deployment["spec"]["template"]["spec"]
    assert pod["automountServiceAccountToken"] is False
    assert pod["nodeSelector"] == {"workload": "app"}
    assert not pod.get("tolerations")
    assert pod["securityContext"]["runAsNonRoot"] is True
    assert pod["securityContext"]["seccompProfile"]["type"] == "RuntimeDefault"
    container = pod["containers"][0]
    assert container["securityContext"] == {
        "allowPrivilegeEscalation": False, "readOnlyRootFilesystem": True,
        "capabilities": {"drop": ["ALL"]},
    }
    assert container["volumeMounts"][0]["readOnly"] is True
    for bound in ("requests", "limits"):
        assert set(container["resources"][bound]) == {"cpu", "memory"}
    env = {item["name"]: item["value"] for item in container["env"]}
    assert env["LAB_HOST"] == "0.0.0.0"
    assert env["LAB_HEALTH_URL"] == "http://llama-cpp.llm.svc.cluster.local:8080/health"
    assert "*" not in env["LAB_ALLOWED_HOSTS"] + env["LAB_ALLOWED_ORIGINS"]
    service = next(item for item in manifest if item["kind"] == "Service")
    assert service["spec"]["type"] == "ClusterIP"
    assert service["spec"]["selector"] == deployment["spec"]["selector"]["matchLabels"]
    assert service["spec"]["ports"][0] == {"name": "http", "port": 80, "targetPort": "http"}
    security = main.TransportSecuritySettings(
        enable_dns_rebinding_protection=True, allowed_hosts=env["LAB_ALLOWED_HOSTS"].split(","),
        allowed_origins=env["LAB_ALLOWED_ORIGINS"].split(","),
    )
    validator = main.TransportSecurityMiddleware(security)
    for hostname in ("lab-info.mcp.svc.cluster.local", "lab-info.mcp.svc.cluster.local:80"):
        request = main.Request({"type": "http", "headers": [(b"host", hostname.encode())]})
        assert asyncio.run(validator.validate_request(request)) is None
    for probe, path in (("livenessProbe", "/healthz"), ("readinessProbe", "/readyz")):
        assert container[probe]["httpGet"]["path"] == path
        headers = container[probe]["httpGet"]["httpHeaders"]
        request = main.Request({"type": "http", "headers": [(b"host", headers[0]["value"].encode())]})
        assert asyncio.run(validator.validate_request(request)) is None


def test_approved_dependency_and_container_sources():
    project = tomllib.loads(Path("pyproject.toml").read_text())
    assert project["tool"]["uv"]["index"] == [{
        "name": "approved", "url": "https://packagefeedproxy.microsoft.io/pypi/simple", "default": True,
    }]
    locked = tomllib.loads(Path("uv.lock").read_text())
    for package in locked["package"]:
        if "registry" in package["source"]:
            assert package["source"]["registry"] == "https://packagefeedproxy.microsoft.io/pypi/simple"
        for artifact in package.get("wheels", []) + ([package["sdist"]] if "sdist" in package else []):
            parsed = urlsplit(artifact["url"])
            assert parsed.scheme == "https"
            assert parsed.hostname in {"packagefeedproxy.microsoft.io", "ms-feed-25.pkgs.visualstudio.com"}
            assert parsed.username is None and parsed.password is None
            assert artifact["hash"].startswith("sha256:")
    sdk = next(package for package in locked["package"] if package["name"] == "mcp")
    assert sdk["version"] == "1.30.0"
    dockerfile = Path("Dockerfile").read_text()
    assert "--frozen --no-dev" in dockerfile
    assert "--index-url https://packagefeedproxy.microsoft.io/pypi/simple --require-hashes" in dockerfile
    assert "uv==0.11.24 --hash=sha256:6ecdad43e870f88d3772d9d37e877259ae35ec374d51589805cdcf6196205829" in dockerfile
    assert dockerfile.splitlines()[0] == "FROM --platform=$BUILDPLATFORM python:3.12.15-slim-bookworm@sha256:6a0e06f5ba0b373d051aabd3fffb9b873f27f9a2a3a14bcbe37dee6f0e3bbc70 AS requirements"
    assert "uv export --offline --frozen --no-dev --no-emit-project" in dockerfile
    assert "COPY --from=requirements /app/requirements.txt ./" in dockerfile
    assert "--require-hashes -r requirements.txt" in dockerfile
    assert "USER 10001:10001" in dockerfile
    assert "pypi.org" not in dockerfile
    assert "files.pythonhosted.org" not in dockerfile
    assert "**" == Path(".dockerignore").read_text().splitlines()[0]