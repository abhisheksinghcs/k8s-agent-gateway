# Project Constitution

## Purpose

This repository provides a reproducible engineering lab for experimenting
with GPU-accelerated local/open-weight AI models on Azure Kubernetes
Service (AKS), llama.cpp, agentgateway, and related agent infrastructure.

The project is intended for:

- hands-on experimentation;
- architecture exploration;
- AI and agent demonstrations;
- GPU-backed local model inference;
- gateway and model-routing experimentation;
- repeatable technical learning.

This is an engineering lab, not a production platform.

However, the lab should demonstrate sound engineering practices and
remain understandable, reproducible, secure, and maintainable.

---

# 1. Repository Is the System of Record

Important project knowledge MUST survive individual human and AI-agent
sessions.

Do not rely on conversational history for durable project state.

The repository is authoritative.

Persistent project knowledge is divided across:

- `PROJECT_CONSTITUTION.md` - governing principles;
- `STATUS.md` - current project state;
- `docs/architecture.md` - implemented and intended architecture;
- `docs/decisions.md` - engineering decisions and rationale;
- `docs/troubleshooting.md` - operational discoveries and failures;
- Git history - actual changes over time.

A new engineer or AI agent with no prior conversation history should be
able to continue the project by reading these artifacts.

---

# 2. Evidence Over Assumption

Working configuration must be proven through observable evidence.

Use these lifecycle states consistently:

PLANNED
CREATED
DEPLOYED
VALIDATED
FAILED

Definitions:

## PLANNED

The component or change is intended but has not yet been implemented.

## CREATED

Required source files, configuration, manifests, scripts, or
infrastructure definitions exist.

## DEPLOYED

The component has been successfully introduced into its target
environment.

## VALIDATED

The intended behavior has been independently demonstrated through an
appropriate test.

## FAILED

The attempted operation or validation did not achieve the intended
result.

Examples:

A Kubernetes manifest existing is CREATED.

A successful `kubectl apply` may mean DEPLOYED.

A running pod does not necessarily mean its application works.

A successful llama.cpp inference request can provide evidence that model
inference is VALIDATED.

A successful direct llama.cpp request does not prove that the
agentgateway routing path is VALIDATED.

Never mark a component VALIDATED solely because configuration or
deployment succeeded.

---

# 3. Understand Before Changing

Agents and engineers must understand the current system before making
meaningful changes.

Before substantial work:

1. Read this constitution.
2. Read `STATUS.md`.
3. Review `docs/architecture.md`.
4. Review relevant decisions.
5. Inspect relevant implementation.
6. Inspect current system state when available.
7. Understand what is already known to work.

Do not replace working infrastructure merely because another approach
appears stylistically preferable.

Changes should have a technical reason.

---

# 4. Reproducibility

Infrastructure and configuration should be reproducible wherever
practical.

Prefer:

- Bicep for Azure infrastructure;
- declarative Kubernetes configuration;
- scripts for repeatable operations;
- parameters and environment variables for environment differences;
- versioned configuration;
- deterministic validation procedures.

Avoid undocumented manual configuration.

If an unavoidable manual operation is required, document it.

A future engineer should be able to recreate the environment without
reverse engineering the original deployment.

---

# 5. Security by Default

Security controls should be proportional to an experimental engineering
lab while preserving good security practices.

Prefer:

- private/internal service exposure;
- managed identities;
- least privilege;
- explicit network exposure;
- Kubernetes Secrets for runtime secrets where appropriate;
- minimal container privileges;
- clearly defined trust boundaries.

Avoid unnecessary production complexity that provides little value to
the lab.

When security requirements differ between:

- experimental lab;
- customer demonstration;
- production environment;

document those differences explicitly.

---

# 6. Public Repository Safety

Assume every committed repository file is publicly readable.

Never commit:

- passwords;
- access tokens;
- API keys;
- private keys;
- Azure credentials;
- kubeconfig credentials;
- model-provider credentials;
- Hugging Face tokens;
- customer information;
- non-public organizational information;
- private environment configuration.

Environment-specific sensitive configuration belongs outside Git or in
an appropriate secret-management mechanism.

Before committing changes, consider whether the content is appropriate
for a public repository.

---

# 7. Separate CPU and GPU Responsibilities

GPU resources are specialized and expensive.

The architecture should intentionally distinguish between:

- Kubernetes/system workloads;
- CPU application workloads;
- GPU inference workloads.

GPU nodes should not become general-purpose scheduling targets
accidentally.

GPU workloads should explicitly request GPU resources and follow the
documented scheduling design.

Changes to GPU scheduling behavior must be documented.

---

# 8. Prefer Private Exposure

Services should default to internal/private exposure.

External access must be intentional.

When exposing services externally:

1. document why external exposure is needed;
2. identify the trust boundary;
3. review authentication requirements;
4. review network exposure;
5. record the architecture decision.

Temporary debugging exposure should not silently become permanent
architecture.

---

# 9. Optimize for Understandability

This project should favor clarity over unnecessary abstraction.

Optimize in this order:

1. understandability;
2. reproducibility;
3. debuggability;
4. security;
5. testability;
6. observability;
7. easy teardown;
8. easy experimentation.

Do not introduce abstraction simply because it might be useful someday.

Build what the project currently needs while leaving reasonable
extension points.

---

# 10. Prefer Small, Reversible Changes

Make focused changes whenever practical.

During troubleshooting, avoid changing several unrelated variables at
the same time.

Use the pattern:

OBSERVATION
-> HYPOTHESIS
-> TEST
-> RESULT
-> CONCLUSION

Clearly distinguish observations from hypotheses.

Before risky changes, understand the last known good state.

Prefer changes that can be rolled back.

---

# 11. Failures Are Project Knowledge

Failed attempts provide useful engineering evidence.

Do not hide them.

For meaningful failures, record:

- what was attempted;
- what happened;
- important error information;
- likely explanations;
- what was ruled out;
- recommended next investigation.

Do not repeatedly retry a documented failed solution unless new evidence
suggests the outcome may differ.

---

# 12. Architecture Decisions Require Rationale

Meaningful design decisions should be recorded in
`docs/decisions.md`.

Important decisions include:

- Azure architecture;
- AKS topology;
- node pool design;
- GPU scheduling;
- model storage;
- model and quantization selection;
- networking;
- identity;
- authentication;
- service exposure;
- llama.cpp configuration;
- agentgateway configuration;
- observability;
- significant security choices.

Document:

- context;
- options considered;
- decision;
- rationale;
- tradeoffs;
- when the decision should be revisited.

The objective is not bureaucratic documentation.

The objective is preventing future engineers and agents from having to
rediscover reasoning.

---

# 13. Separate Implementation From Validation

A component should not validate itself merely by being implemented.

Responsibilities should remain conceptually separate.

Developer:

"I implemented and deployed the component."

Tester:

"I independently demonstrated that the intended behavior works."

Security Reviewer:

"I independently reviewed the relevant security characteristics."

Architect:

"The evidence demonstrates that the milestone satisfies its acceptance
criteria."

Not every trivial change requires all four roles.

Use separation of duties where it materially improves confidence.

---

# 14. Documentation Is Part of the Change

Documentation is not cleanup work performed after engineering.

When project state changes:

update `STATUS.md`.

When architecture changes:

update `docs/architecture.md`.

When an important decision occurs:

update `docs/decisions.md`.

When troubleshooting produces reusable knowledge:

update `docs/troubleshooting.md`.

Important reasoning must not exist only in conversation.

---

# 15. STATUS.md Must Reflect Reality

`STATUS.md` is the primary handoff artifact between engineering and AI
agent sessions.

It must represent what is true now.

It should identify:

- current phase;
- what has been created;
- what has been deployed;
- what has been validated;
- what has failed;
- current blockers;
- relevant evidence;
- last known good state;
- next actions.

Do not record intended work as completed work.

When documentation conflicts with observed system state, correct the
documentation.

---

# 16. Use Authoritative Sources

For technologies whose configuration may change, consult current
authoritative documentation rather than guessing.

This is especially important for:

- Azure;
- AKS;
- NVIDIA GPU integration;
- Kubernetes;
- llama.cpp;
- agentgateway.

Do not invent:

- APIs;
- Kubernetes resources;
- configuration attributes;
- CLI parameters;
- integrations;
- product capabilities.

When desired behavior is unsupported or unclear, document that
limitation.

---

# 17. No Silent Architectural Changes

Agents may identify better architectures.

They should not silently rewrite the project's architecture.

For significant architectural changes:

1. identify the problem;
2. explain the proposed change;
3. identify alternatives;
4. evaluate impact;
5. record the decision;
6. update architecture documentation;
7. update implementation.

Architectural evolution should remain traceable.

---

# 18. Agent Independence

Specialized agents should reason independently within their roles.

A Tester should not assume something works because the Developer says
it works.

A Security Reviewer should not assume something is secure because the
Developer intended it to be secure.

The Architect should evaluate evidence rather than simply aggregating
claims.

Agent specialization exists to increase engineering quality, not merely
to simulate organizational roles.

---

# 19. Avoid Agent Theater

Do not create a separate agent for every technology.

Create specialization only when the role:

- has meaningfully different responsibilities;
- benefits from independent reasoning;
- requires different operational boundaries; or
- provides independent validation.

The initial roles are:

- Architect;
- Developer;
- Tester;
- Security Reviewer.

Additional roles require a demonstrated need.

---

# 20. Human Authority

AI agents assist with engineering work.

They do not own the project.

Human instructions take precedence over agent recommendations.

Potentially destructive operations should be highlighted clearly before
execution when practical.

Agents should optimize for helping the human understand and control the
environment rather than making the environment dependent upon AI.

---

# Final Principle

At any point, another competent engineer or AI agent should be able to
open this repository and determine:

1. What are we building?
2. Why does the architecture look this way?
3. What currently exists?
4. What currently works?
5. What currently fails?
6. What has already been attempted?
7. What evidence supports our claims?
8. What should happen next?

If the repository cannot answer those questions, the project is not
sufficiently documented.