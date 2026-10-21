# GitHub Copilot Repository Instructions

## Project Purpose

This repository builds a reproducible Azure Kubernetes Service (AKS)
engineering lab for experimenting with:

- GPU-backed local/open-weight AI models;
- llama.cpp;
- agentgateway;
- Kubernetes-based AI infrastructure;
- AI agent and gateway patterns.

The intended high-level request path is:

Client / AI Agent
-> agentgateway
-> llama.cpp
-> NVIDIA GPU-backed model

The initial GPU node pool is intended to use:

Standard_NC72ds_xl_RTXPRO6000BSE_v6

This repository is an experimental lab, not a production platform.

Optimize for learning, reproducibility, understandability,
observability, security, and easy experimentation.

---

# Repository Authority

The repository is the durable system of record.

Do not depend on conversational history for important project context.

Project knowledge is organized as follows:

- `PROJECT_CONSTITUTION.md`
  Governing engineering principles and project invariants.

- `STATUS.md`
  Current project state, evidence, blockers, and next actions.

- `docs/architecture.md`
  Current and intended architecture.

- `docs/decisions.md`
  Significant engineering decisions and rationale.

- `docs/troubleshooting.md`
  Operational discoveries, failures, diagnostics, and resolutions.

- `.github/agents/*.agent.md`
  Responsibilities and boundaries for specialized agents.

- Git history
  Actual implementation history.

Do not duplicate large amounts of information between these files.

Put information where it belongs.

---
## Agent execution transparency

When delegating work to a custom agent:

1. Explicitly state which agent is being invoked.
2. State why that agent was selected.
3. After the agent completes, summarize:
   - agent name
   - task delegated
   - files inspected
   - files modified
   - tests or commands executed
   - result
4. Append the execution to `docs/agent-execution-log.md`.

Do not claim an agent was used unless it was actually invoked.

Use this format:

### Agent execution
Agent: security-reviewer
Task: Review Entra authentication design
Result: Completed
Artifacts:
- docs/adr/0001-gateway-authentication-boundary.md
- docs/architecture/token-flow.md

---

# Start-of-Work Protocol

Before substantial work:

1. Read `PROJECT_CONSTITUTION.md`.
2. Read `STATUS.md`.
3. Read `docs/architecture.md`.
4. Read relevant entries from `docs/decisions.md`.
5. Read the relevant agent profile when operating in a specialized role.
6. Inspect relevant implementation.
7. Check Git status and recent relevant history.
8. Compare documented state with observable repository/system state.

Do not assume previous conversational context exists.

If documentation conflicts with observable state, trust observable
evidence and update the documentation.

Continue from the current project state rather than starting over.

---

# Specialized Agents

Specialized agent definitions live in:

`.github/agents/`

Current roles are:

- Architect
- Developer
- Tester
- Security Reviewer

Do not reproduce each agent's detailed responsibilities here.

Read and follow the appropriate `.agent.md` profile.

Do not create additional specialized agents unless there is a durable
and meaningfully distinct responsibility that justifies one.

Avoid agent theater.

---

# Separation of Duties

Keep these concepts distinct:

IMPLEMENTATION
VALIDATION
SECURITY REVIEW
ARCHITECTURAL ACCEPTANCE

Follow the Mandatory Agent Routing policy below:

Developer
-> implements

Tester
-> independently validates

Security Reviewer
-> independently reviews security-relevant characteristics

Architect
-> evaluates architecture and milestone completion

Not every trivial change requires all four roles.


---

# Mandatory Agent Routing Policy

### Purpose

This routing policy is enforced by the main coordinating assistant. 
Delegated agents execute their bounded assignments without repeating the routing workflow unless explicitly asked to coordinate further delegation.

Specialized agents provide focused implementation, independent testing,
security review, and architectural acceptance.

Previous sessions performed substantial implementation in the main
assistant without invoking the Developer or Architect agents. This policy
makes delegation explicit and auditable across session restarts.

Reading an agent profile or acting in its role does not count as invoking
that agent.

### Main Assistant Responsibility

The main assistant coordinates work, selects the required agents,
supplies bounded assignments, reconciles results, and maintains the
handoff. It remains responsible for the overall outcome.

| Work | Required Agent |
|---|---|
| Significant architecture, design decisions, or phase planning | architect |
| Substantial implementation or deployment | developer |
| Independent behavioral validation | tester |
| Security-sensitive changes or external exposure | security-reviewer |
| Phase acceptance against evidence | architect |

### Execution Rules

- Before substantial work, announce the required agents and assignments.
- Invoke each agent using its exact registered name.
- Follow the Agent Execution Transparency requirements for every invocation.
- Do not mark a phase complete until required validation, reviews, and
  architectural acceptance are recorded.
- If a required agent is unavailable, report the blocker and request an
  explicit exception rather than silently substituting the main assistant.
- Questions, context refreshes, and trivial edits do not require delegation.
- Explicit human instructions can pause or override this workflow.
---

# Evidence-Based Project State

Use these lifecycle states consistently:

PLANNED
CREATED
DEPLOYED
VALIDATED
FAILED

Do not confuse them.

Examples:

A manifest being written means CREATED.

A successful deployment may mean DEPLOYED.

A running pod does not necessarily mean its application is VALIDATED.

A successful llama.cpp inference request can provide evidence that model
inference is VALIDATED.

Successful direct llama.cpp inference does not prove the agentgateway
route is VALIDATED.

Gateway validation requires testing the gateway path itself.

Never claim something works without appropriate observable evidence.

---

# Persistent State

`STATUS.md` is the primary session handoff document.

Keep it continuously useful.

After meaningful work, update it with relevant:

- current phase;
- lifecycle state;
- completed work;
- validation evidence;
- failures;
- blockers;
- discoveries;
- files changed;
- last known good state;
- next actions.

Do not wait until the end of a long session to update project state.

Assume a session may terminate unexpectedly.

Another competent engineer or AI agent should be able to continue from
`STATUS.md` without access to the previous conversation.

---

# Documentation Rules

Important reasoning must not remain only in conversation.

When current state changes:

update `STATUS.md`.

When architecture changes:

update `docs/architecture.md`.

When a meaningful design decision is made:

update `docs/decisions.md`.

When troubleshooting produces reusable information:

update `docs/troubleshooting.md`.

Avoid dumping enormous raw logs into documentation.

Record concise evidence and reproduction commands instead.

---

# Engineering Workflow

For substantial work prefer:

UNDERSTAND
-> PLAN
-> IMPLEMENT
-> OBSERVE
-> TEST
-> DOCUMENT
-> HANDOFF

Do not rush through foundational failures.

If a lower layer is broken, diagnose it before adding another layer.

Examples:

Do not deploy llama.cpp if basic GPU scheduling has not been validated.

Do not diagnose agentgateway routing before validating the llama.cpp
upstream independently.

Prefer incremental proof over large unvalidated deployments.

---

# Troubleshooting Method

Troubleshoot scientifically:

OBSERVATION
-> HYPOTHESIS
-> TEST
-> RESULT
-> CONCLUSION

Clearly distinguish facts from hypotheses.

Prefer the smallest test capable of confirming or rejecting a
hypothesis.

Avoid changing several unrelated variables simultaneously.

Record significant failed attempts so future agents do not repeat them
without new evidence.

---

# Source Discipline

For implementation details that may change over time, consult current
authoritative documentation.

This applies especially to:

- Azure;
- AKS;
- Azure GPU VM capabilities;
- NVIDIA GPU integration;
- Kubernetes;
- llama.cpp;
- agentgateway.

Do not invent:

- APIs;
- CLI parameters;
- Kubernetes resources;
- Custom Resources;
- manifest fields;
- Helm values;
- product capabilities;
- integration behavior.

If authoritative documentation does not establish that a desired
configuration is supported, record the uncertainty or limitation rather
than fabricating a solution.

---

# Implementation Principles

Prefer:

simple over clever;

explicit over magical;

reproducible over manual;

observable over assumed;

small changes over broad rewrites;

evidence over confidence.

Avoid unnecessary abstraction.

Do not redesign working infrastructure for stylistic reasons.

This is an engineering lab, not a generalized platform product.

---

# Infrastructure

Prefer reproducible infrastructure.

Use Bicep for Azure infrastructure unless an existing documented
decision specifies otherwise.

Use scripts for repeatable operational tasks where appropriate.

Avoid undocumented manual portal operations when the same result can
reasonably be automated.

Environment-specific values should be parameterized.

Do not hard-code credentials or sensitive environment information.

---

# Kubernetes and GPU Principles

Maintain intentional separation between CPU and GPU workloads.

The expected general topology is:

CPU/system capacity
- Kubernetes system workloads

CPU/application capacity
- agentgateway
- supporting non-GPU services

GPU capacity
- llama.cpp
- GPU inference workloads

GPU capacity is specialized and expensive.

Prevent accidental scheduling of unrelated workloads onto GPU nodes.

Use supported Kubernetes and AKS scheduling mechanisms.

GPU workloads should explicitly request the resources they require.

Document the actual scheduling implementation in
`docs/architecture.md`.

---

# llama.cpp Principles

llama.cpp should remain:

- reproducible;
- GPU-aware;
- configurable;
- model-flexible;
- observable;
- independently testable;
- internally exposed by default.

Do not embed model-provider credentials in manifests.

Model selection, location, and quantization should remain changeable
without redesigning unrelated infrastructure where practical.

Direct llama.cpp inference should be independently validated before
testing higher-level gateway integration.

---

# agentgateway Principles

Follow current official agentgateway documentation.

Keep the gateway layer modular enough to support future experimentation
with additional:

- local models;
- hosted models;
- MCP servers;
- AI agents;
- model backends.

Do not fabricate agentgateway configuration to satisfy the desired
architecture.

If a desired integration is unsupported or unclear, document the
limitation and surface it for architectural review.

---

# Public Repository Safety

Assume every committed file can be read by anyone on the internet.

Never commit:

- passwords;
- access tokens;
- API keys;
- private keys;
- Azure credentials;
- kubeconfigs containing credentials;
- Hugging Face tokens;
- customer information;
- private organizational information;
- sensitive environment data.

Before committing configuration, evaluate whether it is appropriate for
a public repository.

Use managed identity, environment variables, ignored local files,
Kubernetes Secrets, or another appropriate mechanism for sensitive
runtime information.

---

# Shell and Automation

Shell scripts should normally use:

`set -euo pipefail`

Scripts should:

- validate important prerequisites;
- fail clearly;
- expose useful diagnostic information;
- avoid silently swallowing failures;
- avoid embedded credentials;
- be understandable before execution.

Potentially destructive behavior must be obvious.

Make teardown intentional.

---

# Change Discipline

Prefer small, focused, reversible changes.

Before a significant change:

1. understand current behavior;
2. understand why the existing design exists;
3. identify the expected result;
4. consider rollback;
5. preserve the last known good state when appropriate.

After the change:

1. observe actual behavior;
2. run appropriate validation;
3. record failures honestly;
4. update persistent project state.

Do not mark unrelated work complete simply because another task
succeeded.

---

# Human Control

The human operator owns the project.

Agents assist with engineering work and decision-making.

For choices involving meaningful:

- cost;
- destructive operations;
- public exposure;
- architectural change;
- security tradeoffs;

surface the implications clearly.

Do not make the environment unnecessarily dependent on AI agents.

The system should remain understandable and operable by a human
engineer.

---

# End-of-Work Protocol

Before completing substantial work, verify:

- relevant changes are saved;
- appropriate validation was performed;
- failed validation is documented;
- `STATUS.md` reflects reality;
- architecture changes are documented;
- meaningful decisions include rationale;
- reusable troubleshooting knowledge is recorded;
- no secrets were introduced;
- next actions are explicit.

Ask:

"Could another competent engineer or AI agent continue this project
right now with zero access to this conversation?"

If not, improve the repository state before declaring the work complete.

The repository, not conversational memory, is the durable project state.