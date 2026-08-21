---
name: luxonis-app
description: Build or change a Luxonis OAK / DepthAI application. Use when creating, prototyping, developing, implementing, extending, or iterating on an OAK app, including PROJECT_BRIEF, POC_PLAN, and closed-loop validation. Do not use for questions-only, device-only setup, capturing a holistic recording, live inspect of an already-running pipeline, diagnosing a broken existing app, or converting a custom model.
---

# Luxonis App

Turn a business problem into a working DepthAI application and prove it.

## Done when

Replay of a holistic recording shows the brief's success checks on one path
(capture → perception → customer logic → requested output), or **blocked** with one named
next action. Process liveness is not proof. Hardware fault (orange LED, boot failure,
suspected calibration) goes to `support@luxonis.com`.

## 1. Current facts

- Use MCP `luxonis__code` for current APIs, examples, models. Never invent DepthAI APIs from memory. 
- Ensure [oakctl](https://docs.luxonis.com/software-v3/oak-apps/oakctl.md) is installed.
- DepthAI v3 only; do not mix v2 APIs. 
- If MCP is unavailable: `https://docs.luxonis.com/llms.txt`, `oakctl` CLI `--help`.
- Confirm node names from MCP or a current example.

Read the request, the repo, `PROJECT_BRIEF.md`, `POC_PLAN.md`, and `DEVICE.md` when they
exist. Treat `DEVICE.md` as setup notes; trust live state.

## 2. Brief — the business problem

`PROJECT_BRIEF.md` is the customer's problem, not an architecture plan. Use
`assets/PROJECT_BRIEF.template.md`. No pipeline graph, node names, or example names unless
the customer wants those written down.

- **Blank slate:** the user provides the brief. If they already stated the problem, draft
  the file from those facts and ask them to confirm or complete it. If Goal, Scene, Outputs,
  or Success are still missing, give them the template and wait. Do not run a product
  interview to invent the use case.
- **Existing matching brief:** reuse it. Do not restart.
- Patch only when goal, scene, outputs, constraints, or now/later change.

Get a yes on the **use case** before planning a *new* app.

## 3. Plan — how we will build it

For a new app or a change to method, topology, or success checks, write `POC_PLAN.md` from
`assets/POC_PLAN.template.md`. It must include:

- The first-demo boundary and what is deferred
- Starting example, method (deterministic / Zoo / customer model), and topology
- A mermaid pipeline diagram
- A UI or output mockup (overlay layout, JSON payload, or terminal — whatever they see)
- What the recording must contain
- Observable validation checks

Show the plan. Get a yes before implementing a *new* app. Natural approval is enough.

A narrow existing-app edit that does not change method, topology, or success checks does not
need a new plan. Change this repo; do not scaffold a second app.

Prefer a Zoo model or a deterministic method. Custom (not Zoo-ready) model →
`luxonis-model`. Training, dataset collection, proprietary SLAM, or a complete ROS system:
say so and stop. Do not call the OAK use case impossible.

## 4. Recording — close the loop

Iterate against a **holistic recording**, not a live camera session.

If a recording that matches the brief's scene already exists, use it. If it does not, use
`luxonis-record`. Do not copy that procedure here.

- **New app or material redesign:** get the recording before implementing, so you can
  iterate alone.
- **Narrow existing-app edit:** you may apply the requested code change, but do not claim
  success until replay passes.

## 5. Implement and prove on replay

**New app.** Copy the closest current DepthAI v3 example into this project; leave the
reference checkout unchanged. Isolated host environment. Run the example against the
recording when replay supports it. Then make the smallest change that tests the assumption
most likely to kill the approach. Implement one path.

**Existing app.** Change this repo.

Replay via `luxonis-record`. Observe application outputs here: open every image and parse
every structured output used for a claim. When the result leaves the pipeline (MQTT, file,
API, UI), observe that consumer separately. Keep artifacts used for a claim under
`evidence/`.

A live-hardware demo claim still needs the device. For live frames, detections, depth,
crops, or tracks, use `luxonis-inspect`. If the existing app is failing, use
`luxonis-troubleshoot`.

Return to the plan when replay evidence disproves the approach.

## Guardrails

- Ask before sudo, firmware/OS updates, flash, factory reset, Hub adoption, global pip, or
  publishing.
- Approval of a named third-party model revision and license authorizes that download. Cloud
  upload stays a separate explicit ask.
- Never compile DepthAI from source.
- Do not pretend WSL has USB.
- Never run competing processes against one device.
