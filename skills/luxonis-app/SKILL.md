---
name: luxonis-app
description: Build or change a Luxonis OAK / DepthAI application. Use when creating, prototyping, developing, implementing, extending, or iterating on an OAK app — a first-run capability (show depth, stream RGB, run a Zoo model) or a product with docs/brief.md and a dated plan. Do not use for questions-only, workspace bootstrap, device-only setup, capturing a holistic recording, live inspect of an already-running pipeline, diagnosing a broken existing app, or converting a custom model.
---

# Luxonis App

Turn the request into a working DepthAI application and prove it. Ceremony follows the
**request**, not the person.

## Done when

**Capability / first-run:** one real frame or structured message proves the named
capability (live, or replay if a matching recording already exists).

**Product, host-connected path that can holistic-record/replay:** replay of a matching
recording shows the brief's success checks on one path (capture → perception → customer
logic → requested output).

**Product, standalone OAK App or topology that cannot holistic-record:** `luxonis-inspect`
or the installed oakctl run path proves a named claim. State that replay is pending. Do
not hard-stop this skill.

Process liveness is not proof. **Blocked** means one named next action. Hardware fault
(orange LED, boot failure, suspected calibration) goes to `support@luxonis.com`.

## 1. Current facts

Use the Luxonis MCP `code` tool for current APIs, examples, and models. Never invent
DepthAI APIs from memory. DepthAI v3 only; do not mix v2 APIs. Confirm node names from MCP
or a current example.

Best source first: the Luxonis MCP `code` tool, then the exact example or doc source it
returns, then `https://docs.luxonis.com/llms.txt`, then installed CLI `--help`, then
observed behavior; memory is only for general reasoning. If observed host or device
behavior contradicts docs or MCP, trust the observation and note the conflict. If offline,
work from installed `--help` and local examples and name which facts are unverified.

oakctl is required. Prefer `oakctl run-script` for host runs when installed `--help` lists
it as a local DepthAI environment runner; do not invent subcommands. If no host runner
exists, run via the project env and still use oakctl for inspect and udev.

If `AGENTS.md` is missing, or oakctl is missing, name `luxonis-workspace` and follow it, then
continue. Do not copy its procedure.

Read the request, the repo, `docs/brief.md`, `docs/plans/current.md`, and `docs/device.md`
when they exist. Also read legacy root `PROJECT_BRIEF.md`, `POC_PLAN.md`, and `DEVICE.md` if
present; write new work to the `docs/` paths. Treat `docs/device.md` as setup notes; trust
live state.

Stay out of `docs/` for `recordings/`, `evidence/`, application code, `AGENTS.md`, and
`CLAUDE.md`.

## 2. Which path

**Capability / first-run** when the request names a capability without a business
integration or success bar (show depth, stream RGB, run person detection).

**Product** when they named a business outcome, integration (MQTT, unique-once, counting),
accuracy bar, or a matching `docs/brief.md` already exists.

If capability work then becomes a product, write `docs/brief.md` and continue on the product
path.

Prefer a Zoo model or a deterministic method. Custom (not Zoo-ready) model →
`luxonis-model`. Training, dataset collection, proprietary SLAM, or a complete ROS system:
say so and stop. Do not call the OAK use case impossible. When stopping, state what the OAK
side covers, what stays human-owned and the input/output contract between them, and one
next step; record that boundary under Now / later in `docs/brief.md` when a brief exists.

## 3. Capability / first-run

Not gated on a brief or a recording. Implement as below. Prove one real frame or structured
message. If a matching recording already exists, replay it instead of occupying the camera.
Live visual claims (frames, detections, depth, crops, tracks) → `luxonis-inspect`.

## 4. Product — brief

Skip on a capability / first-run request.

`docs/brief.md` is the customer's problem, not an architecture plan. Use
`assets/PROJECT_BRIEF.template.md`. No pipeline graph, node names, or example names unless
the customer wants those written down.

- **Blank slate:** draft `docs/brief.md` from stated facts. Ask at most the load-bearing
  missing facts (where output goes; what success looks like). Defaults are allowed
  (host-connected, overlay or file). Never give them the template and wait. Never invent a
  warehouse/management system.
- **Existing matching brief:** reuse it (including a legacy `PROJECT_BRIEF.md` you just
  read). Do not restart.
- Patch only when goal, scene, outputs, constraints, or now/later change.

Confirm the use case before planning a *new* product app.

## 5. Product — plan

Skip on a capability / first-run request.

For a new app or a change to method, topology, or success checks, write a **dated** plan from
`assets/POC_PLAN.template.md` at `docs/plans/YYYY-MM-DD-<slug>.md`. It must include:

- The first-demo boundary and what is deferred
- Starting example, method (deterministic / Zoo / customer model), and topology
- A mermaid pipeline diagram
- A UI or output mockup (overlay layout, JSON payload, or terminal — whatever they see)
- What the recording must contain
- Observable validation checks

Update `docs/plans/current.md` to a one-line stub pointing at that file. A timestamp without
this pointer is how agents follow a dead plan.

Show the plan. Get a yes before implementing a *new* product app. Natural approval is
enough. A later change to method, topology, or success checks voids that approval; show the
updated plan again.

A narrow existing-app edit that does not change method, topology, or success checks does not
need a new plan. Change this repo; do not scaffold a second app. Do not claim success until
proof.

## 6. Recording and proof

`luxonis-record` owns capture/replay. Do not copy that procedure.

**Host-connected path that can holistic-record/replay:** iterate against a recording.

- **New product app or material redesign:** get the recording before implementing.
- **Narrow existing-app edit:** you may code first; success still needs proof.
- If a matching recording already exists, use it. Do not occupy the camera.

**Standalone OAK App, or topology that cannot holistic-record:** do not hard-stop. Prove with
`luxonis-inspect` (or the installed oakctl run path from `--help`) on a named claim. State
that replay is pending. `luxonis-record` still stops if the topology cannot record — that is
record's job, not a blocker for app "done" here.

## 7. Implement

**New app.** Copy the closest current DepthAI v3 example into this project; leave the
reference checkout unchanged. Isolated host environment. Prefer oakctl for host runs. Then
make the smallest change that tests the assumption most likely to kill the approach.
Implement one path.

**Existing app.** Change this repo.

Observe application outputs: open every image and parse every structured output used for a
claim. When the result leaves the pipeline (MQTT, file, API, UI), observe that consumer
separately. Keep artifacts used for a claim under `evidence/`.

A live-hardware demo claim still needs the device. For live frames, detections, depth,
crops, or tracks, use `luxonis-inspect`. If the existing app is failing, use
`luxonis-troubleshoot`.

Return to the plan when evidence disproves the approach.

## Guardrails

- Ask before sudo, firmware/OS updates, flash, factory reset, Hub adoption, global pip, or
  publishing.
- Approval of a named third-party model revision and license authorizes that download. Cloud
  upload stays a separate explicit ask.
- Never compile DepthAI from source.
- Do not pretend WSL has USB.
- Never run competing processes against one device.
