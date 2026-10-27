"""D-015 contracts: offline manifests first; opt-in real SDK checks later.

These tests protect the bounded MCP-only configuration without contacting AKS,
pulling charts or installing packages. Runtime evidence is separate from source
checks and never confers independent architectural/security acceptance.
"""
import asyncio
import os
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]


def gateway_documents(filename):
    """Read operator-owned gateway inputs, not controller-generated outputs."""
    return list(yaml.safe_load_all((ROOT / "k8s/gateway" / filename).read_text()))


def test_controller_contract():
    """Retain accepted authority and TLS while bounding placement/discovery."""
    values = gateway_documents("controller-values.yaml")[0]
    assert values["nodeSelector"] == {"workload": "app"}
    assert values["tolerations"] == []
    assert values["rbac"]["gatewayNamespaces"] == ["agentgateway-system"]
    assert values["controller"]["xds"]["mode"] == "tls"
    assert values["controller"]["service"]["type"] == "ClusterIP"
    assert "@sha256:" in values["controller"]["image"]["tag"]
    assert values["istio"] == {"enabled": False, "autoEnabled": False}
    for feature in ("inferenceExtension", "agentgatewayModels", "monitoring", "xBackend"):
        assert values[feature]["enabled"] is False


def test_proxy_contract():
    """A Gateway must never transiently inherit an externally exposed Service."""
    parameters = gateway_documents("parameters.yaml")[0]
    spec = parameters["spec"]
    assert spec["service"]["spec"]["type"] == "ClusterIP"
    assert spec["image"]["digest"].startswith("sha256:")
    assert spec["deployment"]["spec"]["replicas"] == 1
    pod = spec["deployment"]["spec"]["template"]["spec"]
    assert pod["nodeSelector"] == {"workload": "app"}
    assert pod["tolerations"] == []
    assert pod["automountServiceAccountToken"] is False
    assert pod["securityContext"]["seccompProfile"]["type"] == "RuntimeDefault"
    security = pod["containers"][0]["securityContext"]
    assert security == {
        "runAsNonRoot": True, "readOnlyRootFilesystem": True,
        "allowPrivilegeEscalation": False, "capabilities": {"drop": ["ALL"]},
    }


def test_single_exact_mcp_route():
    """Disallow implicit prefix/admin/model routing or unexpected tool targets."""
    gateway, backend, route = gateway_documents("gateway.yaml")
    assert {item["metadata"]["namespace"] for item in (gateway, backend, route)} == {"agentgateway-system"}
    assert gateway["spec"]["gatewayClassName"] == "agentgateway"
    assert gateway["spec"]["infrastructure"]["parametersRef"]["name"] == "lab-internal"
    assert gateway["spec"]["listeners"] == [{
        "name": "mcp", "protocol": "HTTP", "port": 8080,
        "allowedRoutes": {"namespaces": {"from": "Same"}},
    }]
    assert backend["spec"] == {"mcp": {
        "sessionRouting": "Stateless", "prefixMode": "Never",
        "targets": [{"name": "lab-info", "static": {
            "host": "lab-info.mcp.svc.cluster.local", "port": 80,
            "path": "/mcp", "protocol": "StreamableHTTP",
        }}],
    }}
    assert route["spec"]["rules"] == [{
        "matches": [{"path": {"type": "Exact", "value": "/mcp"}}],
        "backendRefs": [{"group": "agentgateway.dev", "kind": "AgentgatewayBackend", "name": "lab-info"}],
    }]


@pytest.fixture
def live_gateway_url():
    """Only opt-in operator forwarding may perform live I/O; never a public URL.

    The test owns no listeners or workloads. The operator owns the forward and
    must stop it afterward. No Origin is needed by the official non-browser SDK.
    """
    endpoint = os.environ.get("GATEWAY_TEST_URL")
    if not endpoint:
        pytest.skip("set GATEWAY_TEST_URL to an explicitly localhost-bound proxy forward")
    parsed = urlsplit(endpoint)
    assert parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1"}
    assert parsed.path == "/mcp" and not parsed.query and not parsed.fragment
    assert parsed.username is None and parsed.password is None
    return endpoint


def test_live_sdk_contract(live_gateway_url):
    """Use the installed official SDK, not hand-written JSON-RPC happy paths.

    Two independent initializations and repeated calls protect stateless routing
    and unprefixed tool discovery. Health may be unavailable without invalidating
    MCP: it is a bounded observation, never an instruction to restart llama.cpp.
    """
    async def exercise():
        for attempt in range(2):
            async with httpx.AsyncClient(trust_env=False, timeout=20) as client:
                async with streamable_http_client(live_gateway_url, http_client=client) as (reader, writer, session_id):
                    async with ClientSession(reader, writer) as session:
                        initialized = await session.initialize()
                        assert initialized.protocolVersion == "2025-11-25"
                        tools = (await session.list_tools()).tools
                        assert {tool.name for tool in tools} == {"get_lab_overview", "get_model_health"}
                        assert len(tools) == 2
                        assert all(not tool.inputSchema.get("properties") for tool in tools)
                        for repeat in range(2):
                            overview = await session.call_tool("get_lab_overview", {})
                            assert overview.isError is False and overview.structuredContent
                            assert len(overview.structuredContent["models"]) == 4
                            health = await session.call_tool("get_model_health", {})
                            assert health.isError is False
                            assert set(health.structuredContent) == {"status", "reason", "http_status"}
                            assert health.structuredContent["status"] in {"healthy", "loading", "unhealthy", "unknown"}
                            assert session_id() is None
                            print(f"protocol={initialized.protocolVersion} attempt={attempt} repeat={repeat} tools=2 health={health.structuredContent} session_id_present={session_id() is not None}")
    asyncio.run(exercise())


def test_live_path_and_origin_boundary(live_gateway_url):
    """Exact routing must not expose probes/admin/model paths or foreign Origins.

    Do not strip Origin to make this pass. Backend Host allowlists still apply
    to the gateway-generated upstream authority, not the caller's inbound Host.
    """
    base = live_gateway_url.removesuffix("/mcp")
    with httpx.Client(trust_env=False, timeout=10) as client:
        for path in ("/", "/health", "/healthz", "/readyz", "/mcp/", "/v1/models", "/metrics"):
            response = client.get(base + path)
            assert response.status_code == 404
            print(f"unrouted_path={path} status={response.status_code}")
        response = client.post(live_gateway_url, headers={
            "Origin": "https://foreign.invalid", "Accept": "application/json, text/event-stream",
        }, json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-11-25", "capabilities": {},
            "clientInfo": {"name": "d015-negative", "version": "1"},
        }})
        assert response.status_code in {400, 403, 421}
        print(f"foreign_origin_status={response.status_code}")