---
name: luxonis-build-poc
description: "Build a thin, runnable Luxonis/OAK proof of concept from a project brief by adapting a known-good example."
disable-model-invocation: true
argument-hint: "project brief path or application goal"
metadata:
  author: luxonis
  version: "1.0.0"
  status: stable
---

# Luxonis Build POC

Build the **thinnest runnable slice** that demonstrates the brief's core value on a real OAK
device -- by adapting the closest known-good Luxonis example, not by inventing a pipeline from
scratch. One vertical slice that runs end-to-end beats a broad, half-wired app.

End in exactly one state:

- **running-demo** -- the slice runs and shows the brief's core success observation, proven by
  re-running the exact command/snippet you report.
- **blocked** -- cannot reach a running demo locally; report the one blocking layer, the
  evidence, and the next action (e.g. verify a device with `luxonis-device-setup`).

## Core discipline

<critical>
- **Adapt a known-good example; never invent the DepthAI API from memory.** Tie every API
  call to an example you cloned or a docs page you read.
- **Confirm the `depthai` version before writing pipeline code.** Always target DepthAI v3,
  never v2 -- they differ sharply; match the installed major version and never mix v2 API into
  v3 code. In DepthAI v3, `ColorCamera`/`MonoCamera` are deprecated on all platforms (RVC2
  and RVC4 alike) -- use the `Camera` node.
- **One vertical slice first.** Get a single path running end-to-end before adding any second
  behavior, option, or polish.
- **Never compile DepthAI from source.** If that seems required -> **blocked**.
</critical>

## 1. Preflight

Read the working directory and the user's input. If present, read `PROJECT_BRIEF.md` (what to
build) and `DEVICE.md` (a cached record of a previously verified device). Be self-sufficient:
do not assume any sibling Luxonis skill is installed. Resolve the brief first, then the device.

**Brief.** No `PROJECT_BRIEF.md` -> the purpose-built tool is `/luxonis-project-interview` *if
the user has it*; otherwise capture a one-paragraph goal inline (behavior, target, success
observation) and continue. Do not run a full interview here.

**Device.** A running demo executes on real hardware: DepthAI cannot run without a connected
OAK (both RVC2 and RVC4 -- there is no host-only or simulation mode), and replay is an
on-device input source, never a substitute for a device. `DEVICE.md` is a *hint*, not proof a
device is attached, and it can be stale. Resolve the device by live reachability, not by the
presence of the file:

- `DEVICE.md` present -> reconcile it against a quick live check. If the recorded device still
  opens, use it. If a different device is discovered instead, trust live discovery, use it, and
  offer to update `DEVICE.md`.
- `DEVICE.md` absent -> do not assume "no device". Run a minimal reachability probe (can a
  known-good DepthAI snippet open a device and stream one frame). Do only this probe here; if it
  fails in a way that needs real setup work (USB/udev, PoE, adoption), route to
  `/luxonis-device-setup`.
- Device reachable -> build the slice and run it (the normal path to **running-demo**).
- No device reachable -> build the slice and prepare the exact run command, then end
  **blocked**: the slice is code-complete and ready, but proving it needs a verified device --
  run `/luxonis-device-setup`, then re-run this skill.

## 2. Knowledge sourcing

<critical>
For any Luxonis-specific fact (device capabilities, API/SDK, commands, version requirements),
read live docs starting from `https://docs.luxonis.com/llms.txt` and follow its linked `.md`
pages, then web search only if the docs do not cover it. Never answer such facts from model
memory.
</critical>

Use cloned example **code** as the implementation reference -- and only the curated
`oak-examples` repo on its `main` branch, which tracks DepthAI v3. Clone lazily, only when you
are ready to adapt one:

- Create the directory `~/.luxonis/agent-context` (the `.luxonis/agent-context` folder in the
  user's home) if it does not exist.
- Clone `https://github.com/luxonis/oak-examples` over **HTTPS** (never SSH), shallow and
  pinned to `main`, with git's low-speed guard (`http.lowSpeedLimit=1000`,
  `http.lowSpeedTime=60`) so a stalled network aborts instead of hanging. Clone into a
  temporary sibling path (e.g. `oak-examples.tmp`) and rename it into place only on success,
  using commands appropriate to the host shell, so a failed clone never leaves a partial
  checkout behind. If the checkout already exists, refresh it with a fast-forward-only pull
  instead.
- A checkout is usable only if it contains `INDEX.md`. If the clone fails or the directory is
  incomplete, treat examples as **unavailable** and fall back to live docs. Never read a partial
  checkout, and never substitute web-searched, older, or v2-era examples: always DepthAI v3,
  never v2.

Navigate the checkout with its agent-facing catalog: read `INDEX.md` (match the brief to
`Tags`/`Shape`/`Mode`) and `ESSENTIAL_KNOWLEDGE.md` for shared vocabulary, then the chosen
example's `AGENTS.md`, then its `README.md`. With `oakctl` present, `oakctl app examples list`
is an alternative way to browse.

## 3. Choose the run path from the brief

The brief's **desired run location** plus the device family decide the shape:

- **Laptop/computer connected to the camera** -> **host-side script** (`Shape: script`,
  `Mode: host`). Plain Python with `depthai`, run on the host.
- **On the camera, no computer connected** -> **standalone OAK app** (`Mode: standalone`),
  packaged with `oakapp.toml` and run with `oakctl app run`. Requires RVC4/OAK4.

If the target is unclear, ask one question; do not build both. Pick the example whose
`Shape`/`Mode` already matches the chosen path so you adapt, not convert.

## 4. Build one vertical slice

Start from the closest example and change as little as possible to hit the brief's primary
behavior. Install host dependencies only in an **isolated venv** -- never global `pip`, never
edit project deps without approval. For standalone apps, keep the example's `oakapp.toml`
shape and adjust only what the slice needs.

## 5. Verify, then stop

The brief's success criteria define "works". Run the slice and capture the concrete
observation that proves it.

- **Host script:** `python3 main.py` (in the venv) -- observe the expected output/overlay.
- **Standalone app:**

  ```bash
  oakctl app run <app-dir>                 # uses oakapp.toml; add -d <id> to pin the device
  oakctl app run <app-dir> --detach        # then: oakctl app list / app logs / app stop <id>
  ```

When the run fails, fix **one hypothesis at a time** and re-run the same command -- serialize
changes so you never stack edits or run competing device commands. Declare **running-demo**
only on a passing re-run; if you cannot run it (no device/offline), say so plainly and mark
**blocked** -- do not claim a demo that never ran.

Once the slice runs, stop. Record assumptions, the exact run command, and obvious next steps
in chat (or a short `POC_NOTES.md` if the user wants it). Do not broaden scope unprompted.

## Guardrails

- **Gate privileged/persistent actions.** Global `pip`/project-dependency changes, OS update,
  flashing, factory reset, Hub adoption, publishing an app -> confirm first. Building and
  running a dev app locally is fine.
- **Models, not training.** Reuse DepthAI Model Zoo / example models. If the target needs a
  custom model, say dataset/training is required -- do not claim to train one here.
- **WSL USB honesty.** Do not pretend WSL has USB access; stop until the user exposes the
  device or runs from a host with direct USB.
- **Hardware fault** (orange LED, boot failure, suspected calibration) -> **blocked**, contact
  `support@luxonis.com`.
- Something already built is broken/slow/confusing rather than newly built -> that is
  `luxonis-troubleshoot`'s job.

## Docs

- Software hub / getting started -- https://docs.luxonis.com/software-v3.md
- Docs source map -- https://docs.luxonis.com/llms.txt
- `oakctl` CLI (app run/build/manage) -- https://docs.luxonis.com/software-v3/oak-apps/oakctl.md
- `oakapp.toml` configuration -- https://docs.luxonis.com/software-v3/oak-apps/configuration.md
- V2 vs V3 porting -- https://docs.luxonis.com/software-v3/depthai/tutorials/v2-vs-v3.md
- Examples (catalog in `INDEX.md`) -- https://github.com/luxonis/oak-examples
