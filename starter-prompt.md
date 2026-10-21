We are beginning implementation of this project.

Before doing ANY implementation work, bootstrap yourself from the
repository rather than relying on this prompt or prior conversation.

## Step 1: Establish context

Read these files completely:

1. PROJECT_CONSTITUTION.md
2. .github/copilot-instructions.md
3. STATUS.md
4. docs/architecture.md
5. docs/decisions.md
6. docs/troubleshooting.md
7. the relevant .github/agents/*.agent.md files

Then inspect:

- the complete repository structure
- git status
- recent git history
- existing infrastructure, Kubernetes, scripts, and configuration

Treat the repository as the system of record.

Do not assume anything from previous chat sessions.

If STATUS.md does not yet contain meaningful project state, initialize it
before substantial implementation.

Do not start implementation until you understand the current repository.

---

# Objective

Build a reproducible Azure Kubernetes Service lab for experimenting with
GPU-backed local/open-weight models and agent infrastructure.

The intended high-level request path is:

Client / AI Agent
-> agentgateway
-> llama.cpp
-> NVIDIA GPU-backed model

The GPU node pool is intended to use:

Standard_NC72ds_xl_RTXPRO6000BSE_v6

llama.cpp will provide the initial local inference service.

agentgateway will provide the gateway layer.

Official agentgateway Kubernetes documentation:

https://agentgateway.dev/docs/kubernetes/latest/documentation/quickstart/

---

# Working Model

Use the repository's defined multi-agent roles where useful:

Architect
Developer
Tester
Security Reviewer

Do not use multiple agents merely for ceremony.

The Architect should own planning and architectural coherence.

The Developer should perform implementation.

The Tester should independently validate behavior.

The Security Reviewer should review security-relevant changes at
appropriate milestones.

Implementation and validation are separate responsibilities.

---

# Initial Goal

Do NOT attempt to build the entire environment in one uncontrolled pass.

Start by establishing the engineering plan and validating prerequisites.

The expected broad progression is:

Phase 0 - Repository/bootstrap validation

Phase 1 - Azure prerequisites and infrastructure design

Phase 2 - AKS base cluster

Phase 3 - GPU node pool

Phase 4 - NVIDIA/Kubernetes GPU validation

Phase 5 - Model storage strategy

Phase 6 - llama.cpp deployment

Phase 7 - Direct llama.cpp inference validation

Phase 8 - agentgateway deployment

Phase 9 - agentgateway -> llama.cpp integration

Phase 10 - end-to-end inference validation

Phase 11 - security review and hardening appropriate for the lab

Phase 12 - final documentation and repeatability validation

This sequence is a starting plan, not permission to ignore evidence.

Change the sequence only when there is a concrete engineering reason,
and document significant deviations.

---

# First Task

For this first task:

1. Inspect the repository.
2. Read the governing/project-state files.
3. Determine what already exists.
4. Identify missing repository scaffolding.
5. Inspect the intended Azure/AKS design.
6. Verify current authoritative documentation before making assumptions.
7. Identify Azure prerequisites for the requested GPU SKU.
8. Identify quota, region, AKS, GPU-driver/device-plugin, storage, and
   networking questions that must be resolved.
9. Review the current agentgateway Kubernetes documentation.
10. Review the current llama.cpp deployment requirements relevant to
    NVIDIA GPU inference.
11. Produce an implementation plan.
12. Record the plan and actual current state in STATUS.md.
13. Record any architectural decisions that are already justified in
    docs/decisions.md.
14. Update docs/architecture.md with the initial architecture where
    evidence supports it.

Do not fabricate configuration to fill unknowns.

Clearly identify:

FACT
DECISION
ASSUMPTION
HYPOTHESIS
OPEN QUESTION

where doing so improves clarity.

---

# Infrastructure Direction

Unless repository decisions specify otherwise, begin with this design
direction:

AKS cluster

CPU/system node pool
- Kubernetes system services
- small, cost-conscious CPU SKU

CPU/application capacity
- agentgateway
- supporting non-GPU services

GPU user node pool
- Standard_NC72ds_xl_RTXPRO6000BSE_v6
- llama.cpp
- GPU inference workloads

The GPU pool should be protected from accidental general-purpose
scheduling.

Determine the appropriate supported Kubernetes/Azure mechanism rather
than inventing configuration.

Prefer Bicep plus small operational shell scripts.

---

# Critical Validation Rule

Never translate:

"I created it"

into:

"It works."

Maintain the project lifecycle:

PLANNED
CREATED
DEPLOYED
VALIDATED
FAILED

For example:

AKS Bicep written
= CREATED

AKS resources provisioned
= DEPLOYED

kubectl can access the cluster and expected nodes are healthy
= appropriate AKS validation evidence

GPU node successfully created
does NOT automatically mean GPU support is validated

GPU validation requires appropriate observable GPU evidence

llama.cpp pod running
does NOT mean inference is validated

Inference requires an actual successful model request

agentgateway running
does NOT mean gateway integration is validated

Gateway validation ultimately requires an actual:

client
-> agentgateway
-> llama.cpp
-> model

request to succeed.

---

# Documentation and Session Survival

Assume this session can terminate unexpectedly at any point.

STATUS.md must always be useful to the next agent.

After every meaningful milestone update it with:

- current phase
- work completed
- lifecycle state
- evidence
- failures
- blockers
- important discoveries
- files changed
- next action

For design reasoning update:

docs/decisions.md

For operational discoveries update:

docs/troubleshooting.md

For architecture changes update:

docs/architecture.md

Do not leave important reasoning only in chat.

Checkpoint documentation incrementally.

---

# Public Repository Safety

This repository is public.

Before writing ANY repository file, assume anyone on the internet may
eventually read it.

Never commit:

- Azure credentials
- tokens
- passwords
- API keys
- private keys
- kubeconfigs containing credentials
- Hugging Face credentials
- customer information
- private organizational information
- sensitive environment information

Use example parameter files, environment variables, ignored local files,
managed identity, or secret-management mechanisms as appropriate.

Inspect .gitignore before introducing local environmental configuration.

---

# Source Discipline

Do not invent documentation-sensitive implementation details.

For current behavior, verify authoritative documentation for:

- Azure
- AKS
- the requested GPU VM SKU
- NVIDIA GPU integration
- Kubernetes
- llama.cpp
- agentgateway

If documentation does not support the desired implementation, record the
limitation.

Do not fabricate an API, CRD, manifest field, Helm value, CLI parameter,
or product capability just to make the architecture appear complete.

---

# Engineering Style

Prefer:

simple
over clever

explicit
over magical

reproducible
over manual

observable
over assumed

small changes
over enormous changes

evidence
over confidence

documentation
over conversational memory

Do not over-engineer this as a production platform.

This is an experimental lab intended to remain understandable.

---

# Stop Points

Work incrementally.

Do not rush from infrastructure creation directly into llama.cpp and
agentgateway without validating foundational layers.

A good milestone boundary is:

plan
-> implement
-> observe
-> validate
-> document
-> continue

If a foundational validation fails, diagnose that failure before
layering additional components on top.

---

# Begin

Begin now by reading the repository and establishing current state.

Then perform Phase 0 and begin Phase 1.

Before making substantial Azure changes, make sure the repository
contains enough durable state that another agent could continue if the
session stopped immediately after the change.

Do not merely tell me what files I should create.

Work in the repository, create or modify the necessary files, validate
what can be validated, and keep STATUS.md current as you proceed.