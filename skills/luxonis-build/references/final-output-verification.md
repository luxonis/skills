# Verify the final application output

Pipeline evidence and customer output are separate contracts.

1. Identify the exact pipeline message or state feeding the output adapter.
2. Capture direct pipeline evidence that the source value is correct.
3. Observe the requested consumer-facing output independently.
4. Compare identity, timestamp, units, coordinates, schema, deduplication, and delivery semantics.
5. Test at least one negative or no-event case when false output matters.

Examples:

- MQTT: subscribe independently and verify topic, payload, timestamp, and one-event policy.
- File/JSONL: reopen and parse the produced file; verify record count and schema.
- HTTP/API: issue an independent bounded request and inspect the response/body or receiver log.
- UI/browser: exercise the rendered interaction and compare it with the underlying structured data.
- PLC/robotics adapter: verify the documented interface boundary and units; do not claim the
  downstream machine acted unless it was directly observed.

Do not infer external success from a log line saying that a send, write, or render was attempted.
