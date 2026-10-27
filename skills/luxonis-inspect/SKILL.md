---
name: luxonis-inspect
description: Inspect a running DepthAI or OAK pipeline with oakctl inspect (frames, depth, detections, topics). Use when a pipeline is already running and you need live evidence.
---

# Luxonis Inspect

See what a **running** pipeline is actually producing. A topic list is not proof of correct
behavior. Process liveness is not proof.

## Done when

Opened image or parsed message evidence shows the claimed pipeline behavior, or **blocked**
with the missing endpoint, topic, output, or decoder and one next action.

Never invent oakctl flags from memory.

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

Read `docs/brief.md`, `docs/device.md`, and source when present. Also read legacy root
`PROJECT_BRIEF.md` and `DEVICE.md` if present. None is required. Treat `docs/device.md` as
setup notes; trust live state. Do not start a greenfield interview. If the product is wrong,
mention `luxonis-app`.

## 1. Name the claim

State the narrow claim and the minimum topics that can test it. Separate pipeline structure,
sensor/model/depth/crop/track semantics, application state, and final output outside DepthAI.

## 2. Establish the endpoint

Run current `oakctl inspect --help` and the relevant subcommand help before constructing
commands. Confirm flag names and placement against that help; inspection is evolving.

- Local host pipeline: no target option (local default).
- Another host: `--url ws://<host>:<port>`.
- Standalone OAK 4 app: `--device <selector>` or an exact `--url`.

Call the selected option `<target-options>`. It is empty, `--url <url>`, or
`--device <selector>`. The endpoint is never an unnamed positional argument.

RVC2 cannot run a standalone OAK App; inspect the host running its pipeline. Never infer
localhost because `oakctl` happens to run locally.

## 3. Prepare the application only when needed

For an explicitly read-only inspection, do not edit source or restart the application. If
required topics are absent, report the missing instrumentation and the smallest proposed
source change. Source instrumentation is allowed only when this session is already allowed
to change code; then read `references/instrumentation.md`.

## 4. Discover and capture

Start or attach to the application in the intended topology. Use bounded commands of this
shape, then match the installed syntax if it differs:

```bash
oakctl inspect topics <target-options> --timeout 10s
oakctl inspect pipeline <target-options> --timeout 10s
oakctl inspect snapshot --out <evidence-dir> <target-options> --timeout 10s
oakctl inspect frames <image-topic> --count 3 --out <evidence-dir> <target-options> --timeout 10s
oakctl inspect dump <data-topic> --count 5 <target-options> --timeout 10s
```

Use `--seconds` for a bounded temporal sample when count is a poor fit. Never leave an
unbounded inspect process running.

Topics may appear only after the first message. Produce representative input before diagnosing
an absent topic.

`frames` and `snapshot` decode only the encodings that their error lists (oakctl 0.31.1: JPEG,
PNG, BGR/RGB888, GRAY8). They fail on an NV12 camera topic or a RAW16 depth topic, and
`snapshot` fails as a whole when one advertised topic fails. Capture such a topic with
`oakctl inspect dump <topic> --count 1` into a `.jsonl` file: `message.fb` holds `type`,
`width`, `height`, `stride`, and the plane offsets, and `message.data` holds the frame bytes
as base64. Decode it in the project env:

```python
import base64, json
import numpy as np

msg = json.loads(open("<evidence-dir>/<topic>.jsonl").readline())["message"]
fb, raw = msg["fb"], base64.b64decode(msg["data"])
h, w, off = fb["height"], fb["width"], fb.get("p1Offset", 0)
if fb["type"] == "RAW16":  # StereoDepth depth: millimeters by default, 0 = invalid
    stride = fb.get("stride") or w * 2
    depth = np.frombuffer(raw, np.uint16, h * stride // 2, off).reshape(h, stride // 2)[:, :w]
elif fb["type"] == "NV12":
    import cv2
    stride = fb.get("stride") or w
    uv_off = fb.get("p2Offset") or off + h * stride
    y = np.frombuffer(raw, np.uint8, h * stride, off).reshape(h, stride)
    uv = np.frombuffer(raw, np.uint8, h // 2 * stride, uv_off).reshape(h // 2, stride)
    bgr = cv2.cvtColor(np.vstack([y[:, :w], uv[:, :w]]), cv2.COLOR_YUV2BGR_NV12)
```

Create a unique run directory under `evidence/` (not under `docs/`), with a separate
subdirectory per image topic so common frame filenames cannot overwrite each other. Next
session does not depend on `evidence/`.

## 5. Interpret evidence

Open every image and parse every JSON/JSONL record used for a claim. Check dimensions,
encoding, scene content, crop framing, overlay alignment, labels, confidence, coordinates,
units, timestamps, track state, and whether the observation matches the claimed behavior.

A graph and topic list are structural evidence. Snapshot values may be unsynchronized and are
not a substitute for a temporal sample. For an unsupported encoding, use the `dump` path in
step 4; do not change the application merely to conceal an inspector limitation.

When code changes are needed, keep the capture command stable, change one cause, restart, and
rerun the same capture.

## Guardrails

- Never deploy, stop, restart, reset, update, adopt, flash, or change device settings as part
  of a read-only inspection.
- Never run competing processes against one device.
