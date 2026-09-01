---
name: luxonis-record
description: Capture or replay a DepthAI holistic recording of the real scene (camera/IMU sources, DEPTHAI_RECORD, DEPTHAI_REPLAY, enableHolisticRecord). Use when you need a recording so an agent can develop without a live camera, or to replay an existing recording. Do not use for oakctl inspect of a running pipeline, device-only setup, or building the application itself.
---

# Luxonis Record

Capture a **holistic recording** of the real scene, or replay one that already exists.
Stills, screen captures, and unrelated video are not a recording. A file path is not proof
that source frames replay.

Default capture is a **clean source recorder**, not the product app. Record sockets,
resolution, FPS, IMU, and calibration — not barcode logic, MQTT, or NN nodes.

## Done when

A recording is at a known path under `recordings/` and a bounded replay shows real source
frames from it, or **blocked** with the missing device, scene, topology support, or file and
one next action.

## 1. Current facts

Current holistic record/replay tutorial:
https://docs.luxonis.com/software-v3/depthai/tutorials/holistic-record-replay.md. Never
invent DepthAI APIs or flags from memory. DepthAI v3 only.

Best source first: the Luxonis MCP tools (surfaced names vary by host), then the exact example
or doc source they return, then `https://docs.luxonis.com/llms.txt`, then observed behavior;
memory is only for general reasoning. For oakctl commands and flags, the installed
`oakctl --help` outranks docs and MCP: the local version (possibly older or beta) defines what
is possible here, so work from it and suggest an oakctl update when it lacks something current
docs describe. If observed host or device behavior contradicts docs or MCP, trust the
observation and note the conflict. If offline, work from `oakctl --help` and local examples and
name which facts are unverified.

If `AGENTS.md` is missing, or oakctl is missing, name `luxonis-workspace` and follow it, then
continue. Do not copy its procedure.

Read `docs/brief.md`, `docs/plans/current.md`, `docs/device.md`, and source when present. Also
read legacy root `PROJECT_BRIEF.md`, `POC_PLAN.md`, and `DEVICE.md` if present. None is
required. Treat `docs/device.md` as setup notes; trust live state. Do not start a greenfield
interview. If the product is wrong, mention `luxonis-app`.

## 2. Name the scene

State what the recording must contain: targets, motion, lighting, at least one success case
and one hard case. Take this from the brief or current plan when they exist; otherwise ask
only what would change what you film.

If a matching recording already exists, skip capture and prove it replays.

## 3. Current mechanism

Confirm Camera / RecordConfig / IMU names in `scripts/holistic_record.py` against the
current `holistic_record` example. If they differ, update the copied script from that
example. Do not author a new recorder from scratch.

If this topology cannot holistic-record/replay, say so from current docs and stop.

Prefer `oakctl run-script` for host runs when `oakctl --help` lists it as a local DepthAI
environment runner; do not invent subcommands. If no host runner exists, run via the project
env and still use oakctl for inspect and udev. Still copy
`scripts/holistic_record.py` into the project.

## 4. Device

Hardware must already stream. If it does not, `luxonis-device-setup` first. Never run
competing processes against one device. DepthAI v3 must import in the isolated project
env; this script will not run from a plugin checkout that lacks DepthAI.

They operate the physical scene. You may start the recorder when this host can open the
device; otherwise give them the exact command.

## 5. Capture

Copy `scripts/holistic_record.py` into this project if it is not already there. Run it
from the project env (prefer wrapping with `oakctl run-script` when `--help` lists it). Do
**not** record through the PoC or product app.

`DEPTHAI_RECORD` on an existing app is only for when that app's Camera/IMU sources already
match what you need and you are not about to change sockets, resolution, or FPS.

Write a complete, copy-pasteable guide for this desk — not a link dump:

1. Why this recording (later runs do not need the camera).
2. What to film (named from step 2).
3. Exact command, output directory `recordings/` (not under `docs/`).
4. How long / when to stop (`q` or `--seconds`).
5. The expected `.tar` path they should confirm.

Intended shape (match the script `--help` if it differs; wrap with `oakctl run-script` when
available):

```bash
python3 scripts/holistic_record.py --out recordings --seconds 30
```

Wait until the file exists. Do not fake a recording.

## 6. Prove it replays

Bounded replay of that file with the same clean script. Open a source frame. Process
liveness is not proof. Replay loops; do not leave an unbounded process running. Keep a
sample under `evidence/` if you used it for a claim.

```bash
python3 scripts/holistic_record.py --replay recordings/<name>.tar --seconds 5 --save-frame evidence/replay-preview.png
```

When a caller needs to run the **product** app against the recording, use the current
replay env-var from docs (`DEPTHAI_REPLAY`) on that app. Report the recording path and the
exact replay command.

## Guardrails

- Ask before sudo, firmware/OS updates, flash, factory reset, Hub adoption, or global pip.
- Never compile DepthAI from source.
- Do not pretend WSL has USB.
- Never run competing processes against one device.
