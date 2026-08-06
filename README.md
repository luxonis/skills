# Luxonis Agent Skills: V2 Lightweight Draft

> Experimental direction only. This branch has not been benchmarked, tested with customer
> workflows, or validated for release. It is not ready for customer use or merge.

This draft explores the next step for Luxonis agent support: moving from example-level OAK
onboarding to a working, use-case-specific proof of concept that an engineer can evaluate and
extend. The Luxonis MCP supplies current platform facts; the skills add lightweight planning,
implementation, model, troubleshooting, and direct pipeline-verification workflows.

## Proposed skills

| Skill | Purpose |
| --- | --- |
| `luxonis-build` | Plan, build, inspect, and iterate on an OAK proof of concept. |
| `luxonis-device-setup` | Verify one OAK device and its development path. |
| `luxonis-inspect-pipeline` | Capture and interpret bounded live pipeline evidence. |
| `luxonis-troubleshoot` | Diagnose the first reproducible failing OAK layer. |
| `luxonis-convert-model` | Convert and validate an approved model for a named RVC target. |
| `luxonis-integrate-model` | Integrate a validated Zoo model or NN Archive into an OAK app. |

The skills may be invoked directly or selected by a compatible agent from an ordinary OAK build
request. Customers should not need to learn or manually execute a fixed sequence.

## What this draft is testing

- A single lightweight build orchestrator with progressive disclosure instead of many required
  user-facing steps.
- Human review of a diagrammed plan before a new or materially redesigned POC is implemented.
- MCP-backed current context rather than duplicating fast-changing Luxonis documentation.
- Direct pipeline and final-output evidence instead of treating a running process as success.
- Narrow specialist skills that remain useful independently and can be agent-invoked when needed.

See [the architecture](docs/architecture.md) and [the short RFC](docs/v2-lightweight-rfc.md).
The deterministic checks are scaffolding for iteration, not evidence that the approach works with
customers or real devices.

## License

Licensed under the [Apache License 2.0](LICENSE).
