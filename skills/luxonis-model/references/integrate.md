# Integrate an NN Archive

Wire one target-compatible archive into the current application. Keep the change narrow.
Verify exact APIs against a current example from the Luxonis MCP tools.

## Contract

Use NN Archive metadata as the source of truth for inputs, dimensions, layout, dtype, image
type, preprocessing, heads/parser, labels/keypoints, and RVC compatibility. A raw checkpoint
or source ONNX belongs in conversion first.

## Wire one data path

1. Feed the archive the recorded input type, layout, dimensions, color, and preprocessing.
2. Preserve parser/head metadata and label/keypoint order.
3. Connect the parsed output the application actually consumes.
4. Keep frame, detection, crop, depth, track, and secondary inference on one explicit
   timestamped lineage.
5. Expose representative model input/crops, parsed output, and final annotated or state
   output for inspection.

For detection-then-secondary-model pipelines, feed the same filtered detection stream to
dependent tracker and crop paths. Verify current cropper input types instead of assuming
tracklets are accepted.

For counting, require stable track IDs, a defined crossing or zone event, lifecycle policy,
and per-track count-once state. Do not count frame detections as unique objects.

For depth or spatial association, verify alignment target, coordinate frame, units, invalid
depth policy, and ROI aggregation from synchronized lineage.

When archive metadata lacks required postprocessing, stop for an explicit parser decision
rather than guessing raw tensor semantics.

## Verify

Run the smallest representative fixture through the source and integrated paths. Use
`luxonis-inspect` to show that model input/crop matches the archive and scene region, parsed
labels match expected semantics, association remains correct, and downstream state receives
the result.

Without replay or a device, run imports, config parsing, `scripts/validate_nn_archive.py`,
source inference when available, and deterministic host-logic tests. List every pending
hardware claim.

Report changed files, archive path/checksum, exact run command, evidence, passing checks, and
pending checks.
