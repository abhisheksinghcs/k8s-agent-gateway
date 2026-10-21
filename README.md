# k8s-agent-gateway

Reproducible AKS lab for GPU-backed open-weight models: client -> agentgateway -> llama.cpp -> NVIDIA GPU.

Current state, plan and blockers: [STATUS.md](STATUS.md). Design: [docs/architecture.md](docs/architecture.md). Rules for agents and contributors: [PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md).

## Prerequisites check (read-only)

```bash
LOCATION=westus2 ./scripts/preflight.sh
```

No secrets belong in this repository.
