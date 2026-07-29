---
name: luxonis-inspect-pipeline
description: "Prepare a DepthAI v3 app for direct output inspection, then verify what it actually produces with oakctl inspect. Use when adding RemoteConnection/topics to a Luxonis/OAK app or after building or changing one when success depends on observing live pipeline graphs, images, or structured output rather than process or log state."
metadata:
  author: luxonis
  version: "0.1.0"
  status: experimental
---

# Luxonis Inspect Pipeline

Close the build -> run -> observe loop against what a DepthAI v3 app actually produces.
Inspect direct pipeline outputs rather than treating logs, a successful process start, or a
browser screenshot as proof.

End in exactly one state:

- **verified** -- the requested behavior is visible in captured image/data evidence and the
  exact inspection commands are reported.
- **blocked** -- inspection cannot reach or decode the app; report the failing command,
  endpoint, error, and one next action.

## 1. Preflight the inspector and endpoint

Run `oakctl inspect --help`. If the command is unavailable, end **blocked**: this skill requires
an oakctl version with the `inspect` command.

Establish where the DepthAI pipeline process is running before connecting. Use process state,
the app's launch command, deployment state, or the user's statement as evidence; never infer
localhost merely because `oakctl inspect` is running on this computer.

Choose the endpoint from that topology:

- **Host-run pipeline on this computer** -- run the local DepthAI script in parallel with
  `oakctl inspect`. With the app's `RemoteConnection` on its default port, use no selector;
  this connects to `ws://127.0.0.1:8765`. For another local port, add
  `--url ws://127.0.0.1:<port>`.
- **Host-run pipeline on another computer** -- add
  `--url ws://<computer-address>:<port>`.
- **Standalone pipeline on a remote OAK4** -- add `--device <oak4-address>`; oakctl connects to
  port 8765 on that camera. Use `--url ws://<oak4-address>:<port>` when the app exposes a
  non-default port or an exact endpoint is required.

RVC2 cannot run standalone: its pipeline process runs on a host, so inspect that host's
endpoint. An explicit `--url` overrides device resolution.

If the topology or remote OAK4 address is unknown, ask one focused question and wait:

> Is the DepthAI pipeline running as a local script on this computer, on another host, or as a
> standalone app on an OAK4? If it is remote, what is its address?

Completion criterion: `oakctl inspect` responds to help, the pipeline's run location is
established, and the endpoint names that local host, remote host, or OAK4 explicitly.

## 2. Prepare the app for inspection

Read the existing app before editing. Reuse its `RemoteConnection`, pipeline, and real outputs
when present; add only the missing inspection wiring. Confirm the exact API against the
project's installed DepthAI v3 version or a current known-good example.

### Bind the WebSocket for the run topology

Create one `RemoteConnection` before starting the pipeline:

```python
remote = dai.RemoteConnection(
    address=bind_address,
    webSocketPort=8765,
    serveFrontend=False,
)
```

Set `bind_address` from the topology established in step 1:

- Local script inspected only from the same computer -> `"127.0.0.1"`.
- Remote host or standalone OAK4 inspected over the network -> `"0.0.0.0"`.

`"0.0.0.0"` exposes an unauthenticated plain-WebSocket endpoint to reachable peers. Use it
only on a trusted network. Keep port 8765 unless the app has a reason to use another port, and
make the inspector URL match.

### Expose the real outputs

Register topics after building their outputs and before `pipeline.start()`. Use stable,
descriptive names; the agent will pass these names to `frames` and `dump`.

Link a pipeline `Node.Output` directly:

```python
remote.addTopic("camera", camera_output, "images", False)
remote.addTopic("detections", detection_output, "data", False)
```

The fourth argument is `useVisualizationIfAvailable`. Keep it `False` for outputs that the
agent must decode semantically, so the advertised schema and payload remain the real DepthAI
message type.

For structured messages produced by host Python rather than a node, create a bounded
non-blocking queue and send typed DepthAI messages into it:

```python
detections_topic = remote.addTopic(
    "detections",  # topic name
    "data",        # group
    16,            # max queue size
    False,         # non-blocking
    False,         # preserve the real message type
)

# In the app loop:
detections_topic.send(detections_message)
```

Expose the outputs needed to prove the app's behavior, not synthetic substitutes when real
camera, neural-network, depth, or metadata outputs already exist.

### Start, register, and service the pipeline

Keep this order:

```python
pipeline.start()
remote.registerPipeline(pipeline)

while pipeline.isRunning():
    remote.waitKey(50)
    # Continue the app's normal work and send any host-produced topic messages.
```

`registerPipeline` makes the graph available to `oakctl inspect pipeline`. The app must remain
alive and continue servicing its normal loop. Node-linked topics become visible after their
first output; host-fed topics become visible after the first `send`.

Completion criterion: the source contains one topology-correct `RemoteConnection`, every
behavior-relevant real output has a topic, the started pipeline is registered, and the running
loop continues producing messages.

## 3. Confirm the live inspection surface

Start the app in its intended topology, then run the bounded discovery probe:

```bash
oakctl inspect topics <endpoint> --timeout 10s
```

Success is parseable JSON containing every topic needed to verify the user's goal. If the
connection fails, confirm the app process is running and its bind address/port match the
selected endpoint.

Topics appear only after their first message. For an absent topic, let the app produce a
sample and rerun the same command before diagnosing its `addTopic` wiring.

Completion criterion: `topics` returns every image/data stream required by the requested
verification, or the run ends **blocked** with the missing topic and producer/wiring evidence.

## 4. Capture the evidence

Inspect graph structure first, then capture outputs:

```bash
oakctl inspect pipeline <endpoint> --timeout 10s
oakctl inspect snapshot --out <output-dir> <endpoint> --timeout 10s
```

Treat the pipeline graph as structural evidence only. Open every captured image and read every
captured JSON payload relevant to the goal:

- Check image dimensions, content, overlays, and obvious corruption.
- Check structured fields, labels, coordinates, confidence values, timestamps, and their
  relationship to the expected behavior.
- Read the snapshot manifest and account for every expected topic.

Use focused captures when one snapshot cannot prove the behavior:

```bash
oakctl inspect frames <image-topic> --count 3 --out <output-dir> <endpoint> --timeout 10s
oakctl inspect dump <data-topic> --count 5 <endpoint> --timeout 10s
oakctl inspect dump <data-topic> --seconds 3 <endpoint> --timeout 10s
```

`dump` writes JSONL. Captures are bounded by `--count`, `--seconds`, and `--timeout`; keep them
small enough to inspect completely.

Snapshot samples are the first messages received after subscription, not retained "latest"
values, and samples across topics are not synchronized. Use several frames/messages when
timing or correspondence matters.

Completion criterion: every claim in the requested behavior is backed by an opened image or
parsed data record, not merely by topic presence or graph shape.

## 5. Iterate on one observable

When the task includes changing the app, compare the evidence to the requested behavior, change
one cause, restart the app, and rerun the same capture. Keep the command and observation stable
so before/after evidence is comparable.

Use these inspection failures as app feedback:

- Missing topic -> producer has not emitted, `addTopic` is absent/wrong, or the app is on a
  different endpoint.
- Pipeline call fails while topics work -> pipeline was not registered or the service response
  is incompatible.
- Image decoder rejects a topic -> inspect its advertised encoding. The experimental decoder
  supports JPEG, PNG, `BGR888i`, `RGB888i`, `BGR888p`, `RGB888p`, and `GRAY8`; H264/H265,
  NV12/YUV, depth/disparity, and point clouds require another observation path.
- Messages disappear under load -> use a smaller bounded capture; RemoteConnection queues can
  drop data for slow consumers.

Stop at the first passing rerun. Report the endpoint, exact commands, captured paths, and the
specific observations that establish **verified**. If the loop cannot be closed, report
**blocked** without claiming the app works.
