# OAK POC design review

Use this as an attention and evidence router, not as a computer-vision textbook. Apply only rows
that can affect the requested first demo. For every applicable row, make a decision, retrieve the
current Luxonis facts needed to support it, and define a validating observation.

| Use-case signal | Decisions to resolve | Retrieve current evidence about | Validate with |
| --- | --- | --- | --- |
| Small, distant, dense, or fine-detail target | Required target pixels; sensor/output resolution; lens/FOV; full-frame versus region processing | Available sensor modes, camera controls, crop/resize examples | Representative full frame plus target crop at worst useful distance |
| Fast target, moving camera, vibration, or conveyor | Exposure/blur strategy; rolling/global shutter implications; frame rate; illumination | Device sensor characteristics and current camera-control examples | Bounded capture at representative speed, including missed/blurred cases |
| Glare, low light, outdoor, flicker, or large dynamic range | Lighting, placement, exposure/gain, white balance, anti-banding, HDR/polarization assumptions | Current camera features and controls for the named device | Captures across the expected difficult conditions, not only a favorable scene |
| Metric distance, size, volume, or spatial event | Stereo/ToF/spatial/point-cloud/no-depth method; range; alignment; calibration; invalid depth; coordinate frame | Named device depth capabilities and current measurement examples | Known physical references at near, middle, and far working positions |
| Weak texture, occlusion, reflective/absorptive surface, or edge geometry | Depth failure behavior, filtering, ROI aggregation, fallback or rejection rules | Current depth configuration/filtering guidance | Raw/aligned depth and validity over representative surfaces and boundaries |
| Model input is much smaller than source or target occupies little of the frame | Resize/crop/letterbox/warp/tiling/region-proposal strategy; coordinate restoration | Current ImageManip/cropper/multistage examples and model preprocessing | Published model input/crops plus mapped result on the original frame |
| OCR, barcode, pose, classification after detection, or other second stage | Proposal quality; original-frame crop; association; batching; per-stage latency | Current multistage, crop, parser, and tracker patterns | Synchronized proposals, crops, parsed output, and final association |
| Counting, zones, dwell, crossing, or unique events | Tracker lifecycle; event definition; count-once state; lost/reappearing policy | Current tracking examples and output contracts | Track/event timeline proving one event per intended object/action |
| Several streams, depth alignment, replay, or host state | Timestamp lineage; synchronization; blocking policy; queue sizes; drop behavior | Current node/queue/sync APIs and examples | Timestamps/rates at each relevant boundary under expected load |
| Standalone requirement or limited host | RVC family; OAK App support; HostNode versus device node versus external host; required services | Current device/OAK App/HostNode documentation | Run and inspect the exact intended topology without hidden host dependencies |
| FPS, latency, throughput, power, or bandwidth target | Stage budget; bottleneck hypothesis; model variant/precision; transfer/encoding cost; backpressure | Current model benchmarks, device capabilities, encoder/streaming examples | Per-stage rates and end-to-end observation on the target device/path |
| Video recording plus inference or multiple outputs | Encoder placement; stream resolution/rate; storage/network budget; duplicate transfers | Current encoding, streaming, and OAK App examples | Sustained bounded run with stream health, inference rate, and output delivery |
| External API, MQTT, file, browser, PLC, or robot consumer | Schema; delivery semantics; deduplication; retry/error behavior; coordinate/unit contract | Relevant current Luxonis integration examples plus project system contract | Pipeline evidence and a separately observed consumer-facing event/result |

## Review discipline

- Do not include a section merely to show completeness; mark non-applicable dimensions briefly.
- Distinguish requirements from targets and assumptions.
- Do not promise an FPS, precision, or measurement tolerance from documentation alone. Plan the
  smallest target-device observation.
- Prefer one technically coherent architecture. Alternatives belong only where the user must make
  a consequential tradeoff.
- Add a new rule here only after customer/support evidence or clean-agent tests show a repeated,
  material omission that current docs and the base model do not reliably prevent.
