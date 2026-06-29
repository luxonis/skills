---
name: luxonis-build-poc
description: "Build a thin, runnable Luxonis/OAK proof of concept from a project brief by adapting a known-good example."
disable-model-invocation: true
argument-hint: "project brief path or application goal"
metadata:
  author: luxonis
  version: "0.2.0"
  status: draft
---

# Luxonis Build POC

Build the **thinnest runnable slice** that demonstrates the brief's core value on a real OAK
device — by adapting the closest known-good Luxonis example, not by inventing a pipeline from
scratch. One vertical slice that runs end-to-end beats a broad, half-wired app.

End in exactly one state:

- **running-demo** — the slice runs and shows the brief's core success observation, proven by
  re-running the exact command/snippet you report.
- **blocked** — cannot reach a running demo locally; report the one blocking layer, the
  evidence, and the next action (e.g. verify a device with `luxonis-device-setup`).

## Core discipline

<critical>
- **Adapt a known-good example; never invent the DepthAI API from memory.** Tie every API
  call to an example you cloned or a docs page you read.
- **Confirm the `depthai` version before writing pipeline code.** V2 and V3 differ sharply
  (the V2/V3 trap); match the installed major version. On RVC4, `ColorCamera`/`MonoCamera`
  are deprecated — use the `Camera` node.
- **One vertical slice first.** Get a single path running end-to-end before adding any second
  behavior, option, or polish.
- **Never compile DepthAI from source.** If that seems required → **blocked**.
</critical>

## 1. Preflight

Read the working directory and the user's input. If present, read `PROJECT_BRIEF.md` (what to
build) and `DEVICE.md` (the verified target device). Be self-sufficient: do not assume any
sibling Luxonis skill is installed.

- No `PROJECT_BRIEF.md` → the purpose-built tool is `/luxonis-project-interview` *if the user
  has it*; otherwise capture a one-paragraph goal inline (behavior, target, success
  observation) and continue. Do not run a full interview here.
- No verified device (`DEVICE.md` absent and none confirmed) → you can still build the slice
  and prepare the run command, but a running demo needs a device. Recommend
  `/luxonis-device-setup`, or verify against sample media/replay if the brief provides it.

## 2. Knowledge sourcing

<critical>
For any Luxonis-specific fact (device capabilities, API/SDK, commands, version requirements),
read live docs starting from `https://docs.luxonis.com/llms.txt` and follow its linked `.md`
pages, then web search only if the docs do not cover it. Never answer such facts from model
memory.
</critical>

Use cloned example **code** as the implementation reference. Clone lazily — only when you are
ready to adapt one — over **HTTPS** (never SSH), shallow, into the shared context folder, and
keep going if it fails:

```bash
mkdir -p ~/.luxonis/agent-context
# clone only if missing; bound it so an offline/slow network can't hang the build
timeout 120 git clone --depth 1 https://github.com/luxonis/oak-examples \
  ~/.luxonis/agent-context/oak-examples \
  || echo "examples unavailable — continue using live docs; do not hang"
# if already present, refresh without asking:
git -C ~/.luxonis/agent-context/oak-examples pull --ff-only || true
```

Navigate the checkout with its agent-facing catalog: read `INDEX.md` (match the brief to
`Tags`/`Shape`/`Mode`) and `ESSENTIAL_KNOWLEDGE.md` for shared vocabulary, then the chosen
example's `AGENTS.md`, then its `README.md`. With `oakctl` present, `oakctl app examples list`
is an alternative way to browse.

## 3. Choose the run path from the brief

The brief's **desired run location** plus the device family decide the shape:

- **Laptop/computer connected to the camera** → **host-side script** (`Shape: script`,
  `Mode: host`). Plain Python with `depthai`, run on the host.
- **On the camera, no computer connected** → **standalone OAK app** (`Mode: standalone`),
  packaged with `oakapp.toml` and run with `oakctl app run`. Requires RVC4/OAK4.

If the target is unclear, ask one question; do not build both. Pick the example whose
`Shape`/`Mode` already matches the chosen path so you adapt, not convert.

## 4. Build one vertical slice

Start from the closest example and change as little as possible to hit the brief's primary
behavior. Install host dependencies only in an **isolated venv** — never global `pip`, never
edit project deps without approval. For standalone apps, keep the example's `oakapp.toml`
shape and adjust only what the slice needs.

## 5. Verify, then stop

The brief's success criteria define "works". Run the slice and capture the concrete
observation that proves it.

- **Host script:** `python3 main.py` (in the venv) — observe the expected output/overlay.
- **Standalone app:**

  ```bash
  oakctl app run <app-dir>                 # uses oakapp.toml; add -d <id> to pin the device
  oakctl app run <app-dir> --detach        # then: oakctl app list / app logs / app stop <id>
  ```

When the run fails, fix **one hypothesis at a time** and re-run the same command — serialize
changes so you never stack edits or run competing device commands. Declare **running-demo**
only on a passing re-run; if you cannot run it (no device/offline), say so plainly and mark
**blocked** — do not claim a demo that never ran.

Once the slice runs, stop. Record assumptions, the exact run command, and obvious next steps
in chat (or a short `POC_NOTES.md` if the user wants it). Do not broaden scope unprompted.

## Guardrails

- **Gate privileged/persistent actions.** Global `pip`/project-dependency changes, OS update,
  flashing, factory reset, Hub adoption, publishing an app → confirm first. Building and
  running a dev app locally is fine.
- **Models, not training.** Reuse DepthAI Model Zoo / example models. If the target needs a
  custom model, say dataset/training is required — do not claim to train one here.
- **WSL USB honesty.** Do not pretend WSL has USB access; stop until the user exposes the
  device or runs from a host with direct USB.
- **Hardware fault** (orange LED, boot failure, suspected calibration) → **blocked**, contact
  `support@luxonis.com`.
- Something already built is broken/slow/confusing rather than newly built → that is
  `luxonis-troubleshoot`'s job.

## Docs

- Software hub / getting started — https://docs.luxonis.com/software-v3.md
- Docs source map — https://docs.luxonis.com/llms.txt
- `oakctl` CLI (app run/build/manage) — https://docs.luxonis.com/software-v3/oak-apps/oakctl.md
- `oakapp.toml` configuration — https://docs.luxonis.com/software-v3/oak-apps/configuration.md
- V2 vs V3 porting — https://docs.luxonis.com/software-v3/depthai/tutorials/v2-vs-v3.md
- Examples (catalog in `INDEX.md`) — https://github.com/luxonis/oak-examples
