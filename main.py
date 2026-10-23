# A CPU-side MCP information service, not an agent or an inference server.
# Read: operator configuration -> bounded health GET -> two tools -> HTTP startup.
# Static lab context comes from JSON; only health contacts the llama.cpp router.
# SDK 1.30 owns protocol handling. Its known input reflection is accepted ONLY
# for supervised loopback use (D-012); suppressed logs do not sanitize responses.

import asyncio
from contextlib import asynccontextmanager
import json
import logging
import logging.config
import os
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.server.transport_security import TransportSecurityMiddleware, TransportSecuritySettings
from mcp.types import ToolAnnotations
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

APP_LOG = logging.getLogger("lab_mcp")
HEALTH_TIMEOUT = 3.0
HEALTH_LIMIT = 16 * 1024


def health_url(value: str) -> str:
    # Only the operator chooses egress, once at startup; callers supply no URL.
    try:
        parsed = urlsplit(value)
        valid = (parsed.scheme in {"http", "https"} and parsed.hostname
                 and parsed.username is None and parsed.password is None
                 and parsed.path == "/health" and not parsed.query and not parsed.fragment
                 and "?" not in value and "#" not in value
                 and not any(character.isspace() for character in value)
                 and (parsed.port is None or 1 <= parsed.port <= 65535))
        if valid:
            return value
    except ValueError:
        pass
    raise ValueError("Invalid health configuration")


def load_overview(path: Path) -> dict:
    # Preserve the shared ConfigMap JSON layout; omit provenance scaffolding
    # from the tool result. Validate public content before opening the listener.
    try:
        config = json.loads(path.read_bytes())
        overview = {key: config["overview"][key] for key in (
            "purpose", "components", "intended_request_path", "limitations")}
        models = config["presets"]["models"]
        valid = (isinstance(overview["purpose"], str)
                 and isinstance(overview["components"], dict)
                 and all(isinstance(key, str) and isinstance(value, str)
                         for key, value in overview["components"].items())
                 and all(isinstance(overview[key], list)
                         and all(isinstance(value, str) for value in overview[key])
                         for key in ("intended_request_path", "limitations"))
                 and isinstance(models, list) and all(isinstance(model, dict)
                     and all(isinstance(model[key], str) for key in (
                         "id", "repository", "quantization", "description")) for model in models))
        if valid:
            return {**overview, "models": models}
    except (ValueError, TypeError, KeyError, RecursionError):
        pass
    raise ValueError("Invalid lab configuration")


def configure_logging() -> None:
    # Dependency/access diagnostics can echo bodies, URLs and exception text.
    # Only constant lifecycle labels and controlled handler outcomes log.
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": True,
        "handlers": {"null": {"class": "logging.NullHandler"}},
        "root": {"handlers": ["null"], "level": "CRITICAL"},
    })
    APP_LOG.disabled = False
    APP_LOG.propagate = False
    APP_LOG.setLevel(logging.INFO)
    APP_LOG.handlers = [logging.StreamHandler()]


async def observe_health(upstream: str) -> dict:
    # One observation, not a recovery loop or inference/readiness guarantee.
    result = {"status": "unknown", "reason": "invalid_response", "http_status": None}
    try:
        # Overall deadline includes streaming. No redirects, retries, implicit
        # proxies or compression; normal HTTPS certificate verification stays on.
        async with asyncio.timeout(HEALTH_TIMEOUT):
            async with httpx.AsyncClient(
                timeout=HEALTH_TIMEOUT, trust_env=False, follow_redirects=False,
                transport=httpx.AsyncHTTPTransport(retries=0),
            ) as client:
                async with client.stream("GET", upstream, headers={"Accept-Encoding": "identity"}) as response:
                    status = result["http_status"] = response.status_code
                    if response.headers.get("content-encoding", "identity").lower() != "identity":
                        result["reason"] = "unexpected_encoding"
                    elif 300 <= status < 400:
                        result["reason"] = "redirect_rejected"
                    elif status not in {200, 503}:
                        if 400 <= status < 600:
                            result.update(status="unhealthy", reason="http_error")
                    else:
                        body = bytearray()
                        async for chunk in response.aiter_raw(chunk_size=HEALTH_LIMIT + 1):
                            body.extend(chunk)
                            if len(body) > HEALTH_LIMIT:
                                break
                        if len(body) > HEALTH_LIMIT:
                            result["reason"] = "response_too_large"
                        else:
                            payload = json.loads(body)
                            value = payload.get("status") if isinstance(payload, dict) else None
                            if status == 200 and value == "ok":
                                result.update(status="healthy", reason="health_ok")
                            elif status == 503 and value == "loading model":
                                result.update(status="loading", reason="model_loading")
    except (TimeoutError, httpx.TimeoutException):
        result["reason"] = "timeout"
    except (ValueError, UnicodeError, RecursionError):
        result["reason"] = "invalid_response"
    except httpx.HTTPError:
        result["reason"] = "connection_failed"
    return result


def create_app(config_path: Path = Path("config/lab-info.json"), *,
               upstream: str = "http://127.0.0.1:8080/health",
               allowed_hosts: list[str] | None = None,
               allowed_origins: list[str] | None = None):
    # App assembly shares the SDK lifecycle with tests using loopback stubs.
    # Hosts are inbound authorities, not client addresses or egress destinations.
    upstream = health_url(upstream)
    overview = load_overview(config_path)
    hosts = allowed_hosts if allowed_hosts is not None else ["127.0.0.1:8000", "localhost:8000"]
    origins = allowed_origins if allowed_origins is not None else ["http://127.0.0.1:8000", "http://localhost:8000"]
    if not hosts or any(not value or "*" in value for value in hosts + origins):
        raise ValueError("Invalid transport configuration")
    security = TransportSecuritySettings(enable_dns_rebinding_protection=True,
                                         allowed_hosts=hosts, allowed_origins=origins)
    validator = TransportSecurityMiddleware(security)

    @asynccontextmanager
    async def lifespan(server):
        APP_LOG.info("startup")
        try:
            yield
        finally:
            APP_LOG.info("shutdown")

    server = FastMCP("lab-info", stateless_http=True, json_response=True,
                     streamable_http_path="/mcp", transport_security=security,
                     max_request_body_size=65536, lifespan=lifespan)
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                  idempotentHint=True, openWorldHint=False)

    @server.tool(annotations=annotations)
    async def get_lab_overview() -> dict[str, object]:
        """Return configured lab context and model presets, not live deployment discovery."""
        try:
            APP_LOG.info("get_lab_overview ok")
            return overview
        except Exception:
            raise ToolError("Tool execution failed") from None

    @server.tool(annotations=annotations)
    async def get_model_health() -> dict[str, object]:
        """Observe the fixed router /health; never run inference or load models."""
        try:
            result = await observe_health(upstream)
            APP_LOG.info("get_model_health %s", result["reason"])
            return result
        except Exception:
            APP_LOG.info("get_model_health internal_error")
            raise ToolError("Tool execution failed") from None

    # Custom routes need explicit SDK validation; MCP protection does not cover
    # them. Upstream outages must not restart or disable this CPU service.
    @server.custom_route("/healthz", methods=["GET"])
    @server.custom_route("/readyz", methods=["GET"])
    async def probe(request: Request):
        rejection = await validator.validate_request(request)
        return rejection if rejection is not None else JSONResponse({"status": "ok"})

    return server.streamable_http_app()


def main() -> None:
    # Explicit pod binding; localhost is the laptop default. Port changes also
    # change default Host/Origin entries, never the fixed upstream target.
    configure_logging()
    try:
        host = os.environ.get("LAB_HOST", "127.0.0.1")
        port = int(os.environ.get("LAB_PORT", "8000"))
        if host not in {"127.0.0.1", "0.0.0.0"} or not 1 <= port <= 65535:
            raise ValueError("Invalid listener configuration")
        app = create_app(Path(os.environ.get("LAB_CONFIG", "config/lab-info.json")),
            upstream=os.environ.get("LAB_HEALTH_URL", "http://127.0.0.1:8080/health"),
            allowed_hosts=os.environ.get("LAB_ALLOWED_HOSTS", f"127.0.0.1:{port},localhost:{port}").split(","),
            allowed_origins=os.environ.get("LAB_ALLOWED_ORIGINS", f"http://127.0.0.1:{port},http://localhost:{port}").split(","))
    except (ValueError, OSError):
        APP_LOG.info("startup_failed invalid_configuration")
        raise SystemExit(1) from None
    uvicorn.run(app, host=host, port=port, access_log=False, log_config=None, proxy_headers=False)


if __name__ == "__main__":
    main()
