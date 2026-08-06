# OAK failure layers

Read only the sections that can contain the first failed contract.

## 1. Host toolchain

Check the exact interpreter, isolated environment, installed DepthAI version, imports, CLI
versions, architecture, and selected example requirements. Import success does not prove device or
pipeline readiness.

## 2. Device and transport

Check exclusive access, exact target selection, USB/PoE link, power, routing, firewall/VPN, and
RVC2 host versus RVC4 host/standalone path. Do not probe one device concurrently.

## 3. Lifecycle

Check the actual host process or OAK App state, startup stderr, authentication, managed/factory
state, and bounded lifecycle observation. Do not restart, stop, deploy, or replace an unrelated app
without approval.

## 4. Pipeline structure

Check construction, links, pipeline start, `RemoteConnection`, registration, topics, queue
blocking, and current DepthAI v3 API compatibility. A valid graph can produce wrong data.

## 5. Inputs and imaging

Inspect representative camera/replay frames. Verify dimensions, encoding/color, orientation,
timestamp progression, crop, exposure/blur, and scene content before blaming inference.

## 6. Model and depth

For models, check exact archive, target RVC, input shape/layout/type, preprocessing, heads/parser,
labels, and parsed representative output. For depth, check stereo inputs, calibration, alignment,
units, valid/invalid pixels, ROI aggregation, and representative surface/range.

## 7. Association and application state

Check timestamps, synchronization, crop lineage, detection filtering, track lifecycle/identity,
zones, crossings, thresholds, units/coordinates, and count-once state. Use the same filtered
detections for dependent tracker and crop paths.

## 8. Final output

After upstream evidence passes, independently test the terminal, file, MQTT, API, database, UI,
PLC, or robotics adapter. A log that says send/write/render was attempted is not delivery proof.
