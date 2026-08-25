---
name: luxonis-troubleshoot
description: Diagnose a broken or incorrect existing OAK or DepthAI application. Use when an existing app fails, hangs, or gives wrong output.
---

# Luxonis Troubleshoot

Restore an **existing** OAK path. Change one cause, rerun the same observation, and stop at the
first failing layer.

## Done when

The original failed observation passes and the next dependent check still works, or **blocked**
with a named next action. Hardware fault (orange LED, boot failure, suspected calibration)
goes to `support@luxonis.com`.

Use the Luxonis MCP `code` tool for current APIs and examples. Never invent DepthAI APIs
from memory. DepthAI v3 only; do not mix v2 APIs.

Best source first: the Luxonis MCP `code` tool, then the exact example or doc source it
returns, then `https://docs.luxonis.com/llms.txt`, then installed CLI `--help`, then
observed behavior; memory is only for general reasoning. If observed host or device
behavior contradicts docs or MCP, trust the observation and note the conflict. If offline,
work from installed `--help` and local examples and name which facts are unverified.

If `AGENTS.md` is missing, or oakctl is missing when this job needs the host toolchain, name
`luxonis-workspace` and follow it, then continue. Do not copy its procedure.

Read `docs/brief.md`, `docs/device.md`, source, logs, and evidence when present. Also read
legacy root `PROJECT_BRIEF.md` and `DEVICE.md` if present. None is required. Treat
`docs/device.md` as setup notes; trust live state. Do not start a greenfield interview. If
the product is wrong, mention `luxonis-app`.

## 1. Freeze one failure

State one expected observation and the smallest actual result that contradicts it. Preserve
the exact run and observation commands, the device used in this reproduction, topology,
representative input, relevant versions, and complete stderr, frame, or consumer output when
obtainable.

Reproduce once before editing when safe and bounded. For an intermittent failure, collect
several bounded observations and record frequency.

## 2. Locate the first failing layer

Check in order and stop at the first failure:

1. Host toolchain and imports.
2. Device discovery, transport, power, and exclusive access.
3. Host process or OAK App lifecycle.
4. Pipeline construction, links, registration, and topics.
5. Sensor or replay input.
6. Model/archive input, preprocessing, parser, and inference.
7. Synchronization, crops, tracking, geometry, and application state.
8. Requested file, MQTT, API, UI, terminal, or other final output.

If the device path is unverified, use `luxonis-device-setup`. To capture or replay a
holistic recording, use `luxonis-record`. For claims about live frames, detections, depth,
crops, tracks, or structured pipeline messages, use `luxonis-inspect`. Verify external
output separately from pipeline evidence.

A cheap split: can a minimal known-good DepthAI snippet open the device and stream one frame?
If that fails, the layer is device/connection. If it passes, bisect the app against the
closest current example.

Crash/error: rerun under `DEPTHAI_LEVEL=debug`. Bad depth or output: capture a frame. Low FPS:
measure a number.

## 3. Test one hypothesis

Explain why current evidence favors one cause and what result would falsify it. Change one
cause. Keep the reproduction and observation commands stable. Retry an unchanged action no
more than twice; a third attempt needs a new hypothesis or a human decision.

Prefer a bounded repair: align the environment with the selected example; correct one
address, endpoint, queue, topic, link, or blocking read; restore archive input, parser, or
label order; use the same filtered detections for dependent tracking and crop paths.

Do not begin with a broad rewrite, model replacement, device update, or topology change.

## 4. Verify the repair

Rerun the original failed observation. If it passes, rerun the next dependent check so a
local fix does not hide a downstream regression. Report root cause, evidence, changed files,
exact before/after commands, passing checks, and remaining unverified claims.

## Guardrails

- Ask before sudo/admin, firmware/OS updates, flashing, factory reset, Hub adoption,
  persistent networking, global pip, or replacing customer artifacts.
- Never compile DepthAI from source.
- Do not pretend WSL has USB.
- Never run competing processes against one device.
- Training, proprietary SLAM, or a complete ROS system: say so and stop. Do not call the OAK
  use case impossible. State what stays human-owned and one next step.
