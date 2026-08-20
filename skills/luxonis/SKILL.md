---
name: luxonis
description: Help with Luxonis OAK / DepthAI. Use for questions, choosing a camera, getting hardware working, or building and changing an application.
---

# Luxonis

Entry skill for Luxonis work in this session. An app in this folder is not required.

## Done when

This request is done. **Blocked** means one named next action. Hardware fault (orange LED,
boot failure, suspected calibration) goes to `support@luxonis.com`.

## 1. Can we work?

If the MCP tool `luxonis__code` is missing, stop and get the full plugin installed (skills +
MCP at `https://mcp.luxonis.com/mcp`). Skills-only copies do not include MCP. If the tool is
already available, do not announce a health check.

Use `luxonis__code` (JavaScript sandbox over models, examples, and docs) for current Luxonis
facts. Never invent DepthAI APIs from memory. DepthAI v3 only; do not mix v2 APIs. Confirm
current node names from MCP or a current example.

If MCP is configured but a call fails: `https://docs.luxonis.com/llms.txt`, installed CLI
`--help`, optional cache under `~/.luxonis/agent-context/`.

## 2. See what they already asked

Read the request, the repo, `PROJECT_BRIEF.md`, and `DEVICE.md` when they exist. `DEVICE.md`
is setup notes for later sessions: it may list several units and it may be stale. Trust live
state.

If the request already names the job, do that job. If they invoked this skill with nothing to
go on, ask what they need (questions, pick a camera, get hardware working, inspect, fix,
convert a model, or build/change an app). Do not start a product interview to choose the fork.

## 3. Hand off the specialist job

Name the sibling skill and follow it. Do not copy its procedure here.

- Get hardware working for later development → `luxonis-device-setup`
- About to claim live pipeline behavior → `luxonis-inspect`
- The existing app is failing or wrong → `luxonis-troubleshoot`
- They brought a custom model that is not already Zoo-ready → `luxonis-model`

## 4. Questions and advice

Answer from MCP. Choosing which camera to buy or whether a topology fits lives here, not in
device-setup. Do not write `PROJECT_BRIEF.md` for a question.

## 5. Build or change an app

Product work with no brief: write `PROJECT_BRIEF.md` from `assets/PROJECT_BRIEF.template.md`.
Ask only what would change the product. A detailed engineering request may need few or no
questions.

Get a yes on the **use case** before building a *new* app. Do not re-interview when a brief
already matches the request. Patch the brief only when goal, scene, outputs, constraints, or
now/later change. Keep it a product spec: no pipeline graph, node names, or example names
unless the customer wants those written down.

**New app.** Start from the closest current DepthAI v3 example via MCP. Copy it into this
project; leave the reference checkout unchanged. Install host dependencies in an isolated
environment. Prefer a Zoo model or a deterministic method. Prove the example on the intended
host or standalone path when hardware is available. Then make the smallest change that tests
the assumption most likely to kill the approach. Implement one path: capture → perception →
customer logic → requested output. Process liveness is not proof.

**Existing app.** Change this repo. Do not scaffold a new app beside it.

A live demo claim needs hardware unless the user only asked for code. When the requested
result leaves the pipeline (MQTT, file, API, UI), observe that consumer separately.

If the work is model training, dataset collection, proprietary SLAM, or a complete ROS system:
say so and stop. Do not call the OAK use case impossible.

## Guardrails

- Ask before sudo, firmware/OS updates, flash, factory reset, Hub adoption, global pip, or
  publishing.
- Approval of a named third-party model revision and license authorizes that download. Cloud
  upload stays a separate explicit ask.
- Never compile DepthAI from source.
- Do not pretend WSL has USB.
- Never run competing processes against one device.
