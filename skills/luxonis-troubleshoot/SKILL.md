---
name: luxonis-troubleshoot
description: Reproduce, localize, and fix a broken, slow, missing, or incorrect Luxonis OAK, DepthAI v3, OAK App, model, pipeline, or final-output behavior by repairing the first failing contract and rerunning the same observation. Use for an existing OAK application failure or when a build baseline or acceptance check fails. Do not use to add unrelated features, redesign a working architecture without evidence, or debug generic non-OAK software.
---

# Luxonis Troubleshoot

Restore the requested OAK path without broad rewrites or speculative upgrades.

End in one state:

- **resolved:** the original failed observation passes and the next dependent check still works.
- **blocked:** a named prerequisite, permission, hardware fault, missing artifact, or unsupported
  boundary prevents the next controlled test.

## Freeze one failure

Use `POC_PLAN.md`, `POC_REPORT.md`, `DEVICE.md`, source, logs, versions, and evidence when present;
none is a prerequisite. State one expected observation and the smallest actual result that
contradicts it. Preserve:

- Exact run and observation commands.
- Selected device and host/standalone topology.
- Representative fixture or live scene.
- Relevant configuration and dependency versions.
- Complete stderr, structured message, frame, or consumer output when obtainable.

Reproduce once before editing when safe and bounded. For an intermittent failure, collect several
bounded observations and record frequency.

## Locate the first failing contract

Read only the relevant portions of `references/failure-layers.md`. Check in dependency order:

1. Host toolchain and imports.
2. Device discovery, transport, power, and exclusive access.
3. Host process or OAK App lifecycle.
4. Pipeline construction, links, registration, and topics.
5. Sensor or replay input.
6. Model/archive input, preprocessing, parser, and inference.
7. Synchronization, crops, tracking, geometry, and application state.
8. Requested file, MQTT, API, UI, terminal, or other final output.

Stop at the first layer whose expected observation fails. Use `luxonis-inspect-pipeline` for claims
about live frames, detections, depth, crops, tracks, or structured pipeline messages. Verify
external output separately.

## Form and test one hypothesis

Explain why current evidence favors one cause and what result would falsify it. Prefer current
Luxonis MCP/docs, current example source, installed CLI help, archive metadata, and direct runtime
evidence over remembered APIs.

Change one cause. Keep the reproduction and observation commands stable. Preserve a recoverable
known-good state and before/after evidence. Retry an unchanged action no more than twice; a third
attempt requires a new hypothesis or human decision.

Examples of bounded changes:

- Align the isolated environment with the selected current example.
- Correct one address, endpoint, queue, topic, link, or blocking read.
- Restore archive input, preprocessing, parser, label order, or target compatibility.
- Use the same filtered detections for dependent tracking and crop paths.
- Repair the application-to-output adapter after pipeline evidence passes.

Do not begin with a broad rewrite, model replacement, device update, or topology change. If direct
evidence disproves the architecture, return to `luxonis-build` planning and require renewed review.

## Verify the repair

Rerun the original failed observation. If it passes, rerun the next dependent check so a local fix
does not hide a downstream regression. Report root cause, evidence, changed files/configuration,
exact before/after commands, passing checks, and remaining unverified claims.

## Stop conditions

- Ask before sudo/admin changes, firmware/OS updates, flashing, factory reset, Hub adoption,
  persistent networking, global dependency changes, or replacing customer artifacts.
- Stop hardware boot failure, orange LED, electrical fault, or suspected calibration damage at
  `support@luxonis.com`.
- Isolate model training, proprietary SLAM, a complete ROS application, and production/fleet work
  behind explicit interfaces. Do not claim the use case is impossible because this skill does not
  own the subsystem.
- Never compile DepthAI from source for a POC or run competing processes against one device.
