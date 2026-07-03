---
name: luxonis-troubleshoot
description: "Diagnose broken, slow, or confusing Luxonis/OAK apps and device setups."
disable-model-invocation: true
argument-hint: "symptom, error/log, or app path"
metadata:
  author: luxonis
  version: "1.0.0"
  status: stable
---

# Luxonis Troubleshoot

Diagnose a broken, slow, or confusing Luxonis/OAK app or device. This is the general
"something is wrong" entry: **never refuse**, triage, and either fix it or hand off a clean
support packet. Be self-sufficient -- do not assume any other Luxonis skill is installed.
Reference docs and `support@luxonis.com`, not sibling skills.

End in exactly one state:

- **fixed** -- the original symptom is gone, verified by rerunning the same reproduction.
- **support-packet** -- cannot fix locally -> `SUPPORT_PACKET.md` written with the likely
  owner and next action.

## Core discipline

**Change one thing, rerun the same reproduction, observe.** Never stack changes. Never
declare **fixed** without a passing rerun.

## 1. Preflight

Read the working directory and the user's input. If present, read `DEVICE.md` and
`PROJECT_BRIEF.md`. Do not re-interrogate the user about facts a prior session already
captured.

- `DEVICE.md` -- a *hint* of a previously verified device (model/family/connection/id), not
  ground truth. Use it as a starting point, but trust live discovery and debug logs over it:
  DHCP, re-cabling, or re-adoption can make it stale, and when the record disagrees with what
  the device actually reports, believe the live device and note the drift.
- `PROJECT_BRIEF.md` -- tells you what the app is *supposed* to do; sharpens "wrong output".
- The user's symptom, pasted log/error, or app path is the raw repro material. If they gave
  an app path, read it -- it is what you diff against a known-good example.
- Do **not** read `AGENTS.md`/`CLAUDE.md` as diagnostic source; they are agent guidance.

## 2. Reproduce

Pin the symptom to a concrete, rerunnable observation. This observation *is* the definition
of **fixed**.

- Crash/error -> a command that reproduces it. Run it under `DEPTHAI_LEVEL=debug` (escalate
  to `trace`) to surface XLink/connection/pipeline detail.
- Bad depth/output -> a captured frame or short recording showing the problem.
- Low FPS/latency -> a measured number.

Use the smallest reliable repro.

## 3. Isolate: device vs app

One cheap check decides which layer the bug is on: can a minimal known-good DepthAI snippet
open the device and stream one frame?

Live DepthAI discovery is the authority here. `oakctl list` is non-authoritative: RVC2 is
DepthAI-first and never appears in `oakctl` at all, so an empty `oakctl list` is not evidence a
device is missing -- confirm with DepthAI discovery before concluding a device is unavailable.

- **Fails -> device/connection layer.** Do the basic checks yourself, citing the docs
  runbook below. If first-contact setup is the real problem, the purpose-built tool is
  `/luxonis-device-setup` *if the user has it installed* -- otherwise continue here. A
  hardware fault (orange LED, boot failure, suspected calibration) is a hard stop ->
  **support-packet** to `support@luxonis.com`.
- **Passes -> app/pipeline layer.** The device is fine; the bug is in the user's app,
  pipeline, or config. **Bisect against the closest known-good Luxonis example**: if the
  example runs and the app does not, the delta between them *is* the bug.

**Never reason about the DepthAI API from memory.** Confirm every API claim against a
known-good example or the docs, and confirm the `depthai` version before touching
version-sensitive code -- always DepthAI v3, never v2.

For the app-layer diff, use `~/.luxonis/agent-context/oak-examples` as the example reference --
only when a comparison actually helps, not routinely. Source it the same safe way as a build:

- Create the directory `~/.luxonis/agent-context` (in the user's home) if it does not exist.
- Clone `https://github.com/luxonis/oak-examples` over **HTTPS** (never SSH), shallow and
  pinned to `main` (which tracks DepthAI v3), with git's low-speed guard
  (`http.lowSpeedLimit=1000`, `http.lowSpeedTime=60`) so a stalled network aborts instead of
  hanging. Clone into a temporary sibling path (e.g. `oak-examples.tmp`) and rename it into
  place only on success, using commands appropriate to the host shell, so a failed clone never
  leaves a partial checkout behind. If the checkout already exists, refresh it with a
  fast-forward-only pull instead.
- A checkout is usable only if it contains `INDEX.md`. If the clone fails or is incomplete, do
  the diff from live docs instead; never diff against a partial checkout or an older/v2 example.

## 4. Fix one hypothesis at a time

Change exactly one thing, rerun the repro, observe. Add a print/log only if the repro does
not already show the answer.

- Repro passes -> **fixed**.
- A few one-change cycles do not move the repro, or a stop condition is hit -> stop and write
  the packet. Giving up locally is an honorable outcome; do not churn the user's code with
  shotgun edits.

## Symptom -> layer -> docs

Use this only to pick the right repro and the right page fast. The fixes live in the docs.

| Symptom | Layer | Docs |
| --- | --- | --- |
| Device not found / discovery | device | Device Information; OAK4 / USB getting-started |
| Linux USB permissions, PoE / network / LED | device | USB / OAK4 getting-started; troubleshooting index |
| Device bricked / won't boot | device -> support | my-device-is-bricked |
| Pipeline crash / error | app | diff vs known-good example |
| Bad stereo / depth | app | StereoDepth node |
| Low FPS / latency | app | my-app-is-slow; optimizing |
| Neural network issues | app | neural-network-issues |
| V2 / V3 confusion | version | v2-vs-v3 |

## Guardrails

- **Hardware fault -> stop, support.** Orange LED, boot failure, suspected calibration.
- **Never compile DepthAI from source.** If that seems required -> **support-packet**.
- **Gate privileged/persistent actions.** sudo/admin, udev edits, firmware update, flashing,
  factory reset, Hub adoption, global `pip` or project-dependency changes -> confirm first.
  Non-privileged diagnosis (isolated venv, reading logs, rerunning the repro) runs freely.
- **No blind API fixes.** Every DepthAI change tied to a known-good example or docs; confirm
  the SDK version before touching version-sensitive code.
- **Escalate instead of thrashing.** Out of local means -> write the packet.
- **WSL USB honesty.** Do not pretend WSL has USB access; stop until the user exposes the
  device or runs from a host with direct USB.

## Support packet

Write `SUPPORT_PACKET.md` in the current working directory only when local fixing is
exhausted, then tell the user to send it to `support@luxonis.com`.

```md
# Luxonis Support Packet: <one-line symptom>

## Symptom
What's wrong + the concrete repro observation (command output / measured FPS / frame).

## Environment
OS, Python, depthai version, oakctl version if used, connection (USB/PoE),
device model/family/id (from DEVICE.md if present).

## Device state
Discovered? Verified working before? LED state. Managed vs factory.

## What I tried
One line per hypothesis: change -> rerun result.

## Logs / errors
Smallest relevant excerpt (include DEPTHAI_LEVEL=debug output if relevant).

## Likely owner / next action
Best-guess category (device / network / app / depth / performance / version) + next step.
```

`depthai` and `oakctl` versions are mandatory so support can spot V2/V3 issues immediately.
`oakctl` is expected to gain a support-file/bundle command; once it exists, prefer generating
that over the ad-hoc levers above.

## Docs

- Troubleshooting index -- https://docs.luxonis.com/software-v3/troubleshooting.md
- My app is slow -- https://docs.luxonis.com/software-v3/troubleshooting/my-app-is-slow.md
- Device bricked -- https://docs.luxonis.com/software-v3/troubleshooting/my-device-is-bricked.md
- Neural network issues -- https://docs.luxonis.com/software-v3/troubleshooting/neural-network-issues.md
- StereoDepth node -- https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/stereo_depth
- Optimizing performance -- https://docs.luxonis.com/software-v3/depthai/tutorials/optimizing.md
- V2 vs V3 -- https://docs.luxonis.com/software-v3/depthai/tutorials/v2-vs-v3.md
- Device Information -- https://docs.luxonis.com/software-v3/depthai/examples/misc/device_information.md
- OAK4 getting started -- https://docs.luxonis.com/hardware/platform/deploy/oak4-deployment-guide/oak4-getting-started.md
- OAK USB getting started -- https://docs.luxonis.com/hardware/platform/deploy/usb-deployment-guide.md
