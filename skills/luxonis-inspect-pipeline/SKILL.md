---
name: luxonis-inspect-pipeline
description: Prepare and inspect a running DepthAI v3 or OAK application, then verify its real pipeline graph, image frames, depth, detections, crops, tracks, or structured messages with oakctl inspect. Use when an OAK claim depends on live pipeline output, after building or changing a pipeline, or when logs and process state are insufficient. Do not use for generic logging or as proof that an external UI, API, MQTT consumer, or complete customer workflow works.
---

# Luxonis Inspect Pipeline

Close the build, run, observe loop with direct bounded evidence. Inspection proves only the
behavior actually observed.

End in one state:

- **verified:** opened image or parsed message evidence shows the requested pipeline behavior.
- **blocked:** the endpoint, topic, output, or decoder cannot provide the required evidence.

## Define the inspection contract

Use `POC_PLAN.md` when present. Otherwise state the narrow claim being tested and infer the minimum
topics needed to test it. Separate:

- Pipeline structure.
- Sensor/model/depth/crop/track semantics.
- Customer application state.
- Final output outside DepthAI.

Do not require a plan for standalone inspection.

## Establish the endpoint

Run current `oakctl inspect --help` and relevant subcommand help before constructing commands.
Determine where the DepthAI process runs:

- Local host pipeline: use no target option for the local default endpoint.
- Another host: use `--url ws://<host>:<port>`.
- Standalone OAK 4 app: use `--device <selector>` or an exact `--url`.

RVC2 cannot run a standalone OAK App; inspect the host running its pipeline. Never infer localhost
because `oakctl` happens to run locally.

Call the selected option `<target-options>`. It is empty, `--url <url>`, or
`--device <selector>`. The endpoint is never an unnamed positional argument. Confirm placement
against installed help because inspection is evolving.

## Prepare the application only when needed

For an explicitly read-only inspection, do not edit source or restart the application. If required
topics are absent, report the missing instrumentation and the smallest proposed source change.
Source instrumentation is allowed only when inspection comes from an authorized build or
code-change request.

Read the existing source and reuse its `RemoteConnection`, pipeline registration, and topics. Add
only missing behavior-relevant outputs and verify exact APIs against the installed DepthAI v3 or a
current known-good example.

The intended shape is:

```python
remote = dai.RemoteConnection(
    address=bind_address,
    webSocketPort=8765,
    serveFrontend=False,
)
```

Use `127.0.0.1` only for same-host inspection. Binding `0.0.0.0` exposes an unauthenticated plain
WebSocket endpoint to reachable peers; use it only on a trusted path and say so.

Expose stable topics from real outputs:

```python
remote.addTopic("camera", camera_output, "images", False)
remote.addTopic("detections", detection_output, "data", False)
```

Keep original semantic messages when decoding requires them. For host-produced data, use a small
non-blocking topic queue and send typed messages. Start the pipeline, register the pipeline, then
continue the normal application loop.

Do not expose every stream by default and do not create synthetic substitutes for available real
camera, model, depth, or state output.

## Discover and capture

Start the application in the intended topology. Use bounded commands:

```bash
oakctl inspect topics <target-options> --timeout 10s
oakctl inspect pipeline <target-options> --timeout 10s
oakctl inspect snapshot --out <evidence-dir> <target-options> --timeout 10s
oakctl inspect frames <image-topic> --count 3 --out <evidence-dir> <target-options> --timeout 10s
oakctl inspect dump <data-topic> --count 5 <target-options> --timeout 10s
```

Use the syntax shown by the installed version if it differs. Use `--seconds` for bounded temporal
observations when count is unsuitable. Never leave an unbounded inspect process running.

Topics may appear only after the first message. Produce representative input before diagnosing an
absent topic.

## Interpret evidence

Create a unique run directory under `evidence/`, with a separate subdirectory per image topic so
common frame filenames cannot overwrite evidence from another topic. Open every image and parse
every JSON/JSONL record used for a claim. Check:

- Dimensions, encoding, scene content, corruption, crop framing, and overlay alignment.
- Labels, confidence, coordinates, units, timestamps, track state, and application fields.
- Progression across several messages when timing or association matters.
- Whether the observation matches the requested behavior, not merely whether a topic exists.

A graph and topic list are structural evidence. Snapshot values may be unsynchronized and are not
a substitute for a temporal sample. Unsupported H264/H265, NV12/YUV, depth, disparity, or point
cloud rendering may require another bounded observation path; do not change the application merely
to conceal an inspector limitation.

## Report and return

Report endpoint, exact commands, evidence paths, observations per topic, passed/failed pipeline
claims, and every final-system claim still unverified. When code changes are needed, keep the
capture command stable, change one cause, restart, and rerun the same capture.

Never deploy, stop, restart, reset, update, adopt, flash, or change device settings as part of a
read-only inspection request.
