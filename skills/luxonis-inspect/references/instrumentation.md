# Inspection instrumentation

Use this only when this session is already allowed to change application code. Verify exact
APIs against installed DepthAI v3 or a current example from the Luxonis MCP tools.

Read the existing source and reuse its remote connection, pipeline registration, and topics.
Add only missing behavior-relevant outputs. Do not expose every stream by default. Do not
create synthetic substitutes for available real camera, model, depth, or state output.

Intended shape (confirm names and arguments from current source):

```python
remote = dai.RemoteConnection(
    address=bind_address,
    webSocketPort=8765,
    serveFrontend=False,
)
remote.addTopic("camera", camera_output, "images", False)
remote.addTopic("detections", detection_output, "data", False)
```

Use `127.0.0.1` only for same-host inspection. Binding `0.0.0.0` exposes an unauthenticated
plain WebSocket to reachable peers; use it only on a trusted path and say so.

Keep original semantic messages when decoding requires them. For host-produced data, use a
small non-blocking topic queue and send typed messages. Start the pipeline, register it, then
continue the normal application loop.
