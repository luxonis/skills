---
name: luxonis-build
description: Plan, build, run, inspect, and iterate on a use-case-specific Luxonis OAK or DepthAI application until a working proof of concept is observed. Use when the user asks to prototype, build, create, plan, or materially extend an OAK camera application. Do not use for a generic non-OAK coding task, a device-only connection problem, a standalone model conversion, or diagnosis of an already-broken app when a narrower Luxonis skill applies.
---

# Luxonis Build

Build the smallest working OAK demo that exercises the customer's real scene, application
behavior, run topology, and requested output. Use the Luxonis MCP and current known-good examples
for version-sensitive facts. Do not invent DepthAI APIs from memory.

End in one state:

- **awaiting-user-context:** at least one unanswered decision can materially change feasibility,
  hardware, imaging, method, model, topology, external contract, acceptance, or first-demo scope.
  Ask for it and stop. Do not create a new `POC_PLAN.md` or request plan approval.
- **awaiting-plan-approval:** `$PWD/POC_PLAN.md` exists, identifies its revision, contains no
  unresolved Must-ask decision, and is ready for human review. Request review and stop.
- **working-demo:** a repeatable run proves perception, customer logic, final output, and topology.
- **blocked:** one named contract cannot proceed locally; show evidence and the next action.
- **human-subsystem-required:** the supported OAK boundary is ready but a defined external artifact
  or specialist subsystem is required.

## Classify the request

Inspect the request, repository, `POC_PLAN.md`, `DEVICE.md`, `MODEL_CONVERSION.md`, representative
media, tests, and existing evidence before questioning the user.

- **New POC or material redesign:** read `references/plan-poc.md`,
  `references/design-review.md`, and `references/current-context.md`. Plan and stop for review.
- **Plan only:** use the same planning references and stop after plan review is requested.
- **Approved-plan implementation:** verify the approved revision still represents the request,
  then build.
- **Narrow existing-app edit:** work directly when the change does not alter sensor strategy,
  perception method, model contract, run topology, or acceptance behavior. Return to planning if
  the evidence requires a material redesign.

Do not require `PROJECT_BRIEF.md`. Do not force an existing engineer through a generic interview.

## Enforce the plan gate

For a new POC or material redesign, never implement before the user has reviewed the current
`POC_PLAN.md` and clearly approved it. Natural approval such as "looks good, proceed" is enough;
silence, an unrelated reply, or a request containing corrections is not approval. Record approval,
date, and plan revision without changing technical content. Any later technical plan change
invalidates approval.

## Resolve current context and prerequisites

Use the approved plan's example, model, device, and topology. Recheck fast-changing details with
the Luxonis MCP. Use the fallback hierarchy in `references/current-context.md` when MCP is
unavailable or exact example source is needed.

Resolve only required prerequisites:

- Use `luxonis-device-setup` for an unverified device or run path.
- Use `luxonis-convert-model` for an approved external model that lacks a target-compatible NN
  Archive.
- Use `luxonis-integrate-model` when wiring a validated archive is non-trivial.

Specialist activation is model-mediated. Keep the plan gate, evidence standard, and completion
criteria here even when a sibling skill is unavailable.

## Establish the known-good baseline

Start from the current DepthAI v3 example that most closely matches the approved device family,
topology, model task, and observable outputs. Keep the reference checkout immutable and copy only
the selected example into the project.

Run the selected example on the intended path before broad changes. Confirm a direct sensor,
model, or output observation, not only imports or process liveness. Record the command and passing
observation. If the baseline fails, use `luxonis-troubleshoot` before adding application behavior.

## Test the highest-risk supported assumption

Make the smallest planned change that tests the use-case assumption most likely to invalidate the
approach. Use representative replay/media or the smallest repeatable live capture.

- Preserve a passing checkpoint before continuing.
- Return to planning when evidence disproves the architecture.
- Isolate model training, proprietary SLAM, a complete ROS system, or other unsupported specialist
  work behind a concrete input/output contract. Use
  `assets/HUMAN_SUBSYSTEM_HANDOFF.template.md` when that contract must be handed to a specialist.
  Do not claim the OAK use case is impossible merely because this plugin cannot complete that
  subsystem.
- When training data is required, offer a separate collection-app session and use
  `assets/DATA_COLLECTION_HANDOFF.template.md`; do not start that project inside the POC.

## Build the use-case vertical slice

Implement one end-to-end path:

1. Preserve known-good capture and pipeline behavior.
2. Add the primary perception, deterministic algorithm, or validated model path.
3. Expose behavior-relevant frames and structured messages.
4. Add the customer-specific tracking, measurement, filtering, state, or decision logic.
5. Add the requested terminal, file, MQTT, API, UI, or other external output.

Keep data lineage explicit across frames, detections, depth, crops, tracks, and host state. Do not
stop when the generic example runs.

## Run, inspect, and iterate

Use `luxonis-inspect-pipeline` whenever correctness depends on live frames or structured pipeline
output. Retain bounded evidence under `evidence/` and open or parse every artifact used for a claim.
Read `references/final-output-verification.md` when the requested result leaves the DepthAI
pipeline.

Repeat:

1. Run the exact host or OAK App command.
2. Capture the planned pipeline evidence.
3. Verify the external output separately.
4. Compare both with the approved working-demo checks.
5. Identify the first failing layer.
6. Change one supported cause or use `luxonis-troubleshoot`.
7. Restart and rerun the same observation.

Stop for a human decision when controlled attempts stop improving evidence, the architecture is
disproved, scope must change, or the next action is privileged or persistent.

## Finish from evidence

Declare **working-demo** only after a passing rerun proves:

- The planned perception behavior on representative input.
- The customer-specific application behavior.
- The requested final output.
- The intended host-connected or standalone topology.

Write `POC_REPORT.md` from `assets/POC_REPORT.template.md`. Include exact commands, configuration,
input or scene, evidence paths, passing checks, limitations, and human-provided components. Do not
call the POC production-ready.

## Guardrails

- Ask before OS/firmware updates, flashing, factory reset, Hub adoption, global dependency
  changes, persistent networking, cloud upload, or publishing an app, package, model, or artifact
  to Hub, a public registry, or another persistent shared destination.
- Approval of a plan naming an exact third-party model revision and license authorizes its expected
  download. The approved plan also authorizes its named MQTT, API, file, or UI demo output. Do not
  ask again for those actions. A changed model, source, license, upload, or output destination
  requires renewed approval.
- Never run competing processes against one device.
- Never compile DepthAI from source for a POC.
- Stop hardware boot failure, orange LED, electrical fault, or suspected calibration damage at
  `support@luxonis.com`.
