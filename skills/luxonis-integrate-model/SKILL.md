---
name: luxonis-integrate-model
description: Integrate a validated target-compatible Luxonis Model Zoo model or NN Archive into a DepthAI v3 or OAK application while preserving its input, preprocessing, parser, labels, outputs, and data lineage. Use when a compatible archive must be wired or swapped into an OAK pipeline, especially for custom, multi-stage, crop, tracking, or parsed-output integration. Do not use to train or convert a source model, select an unapproved third-party model, or redesign the whole application.
---

# Luxonis Integrate Model

Wire one validated archive into the current application and prove the model path on representative
input. Keep the change narrow.

End in one state:

- **integrated-and-verified:** representative replay/device evidence proves model input, parsed
  output, association, and downstream delivery.
- **code-integrated-awaiting-runtime:** static/source checks pass but required replay or device
  evidence is unavailable.
- **blocked:** archive and application contracts cannot be reconciled without guessing.

## Establish the integration contract

Read the archive, current app, relevant plan, selected example, and `MODEL_CONVERSION.md` when it
exists. Require a target-compatible archive and accepted validation result. Accept
`archive-metadata-valid-awaiting-inference` only when this integration will perform the missing
representative behavior test; do not treat it as archive-ready. A raw checkpoint or source ONNX
belongs in `luxonis-convert-model`.

Use NN Archive metadata as the source of truth for:

- Inputs, dimensions, layout, dtype, image type, and preprocessing.
- Outputs, heads/parser, labels/keypoints, and semantics.
- Target executable and RVC compatibility.

Do not require a conversion report for a compatible Model Zoo archive whose provenance and
metadata are sufficient. Do not hard-code a replacement contract from memory.

## Choose a current reference pattern

Use Luxonis MCP to retrieve the nearest current model integration example and docs. Match task,
archive contract, target family, and runtime topology, not only a model filename. Read only the
relevant section of `references/integration-patterns.md` and verify exact APIs against current
source.

## Wire one coherent data path

1. Feed the archive the recorded input type, layout, dimensions, color, and preprocessing.
2. Preserve parser/head metadata and label/keypoint order.
3. Connect the actual parsed output expected by application logic.
4. Keep frame, detection, crop, depth, track, and secondary inference association on one explicit
   timestamped lineage.
5. Expose representative model input/crops, parsed output, and final annotated/state output for
   inspection.

For detection-to-secondary-model pipelines, feed the same filtered detection stream to dependent
tracker and crop paths. Verify current cropper input types instead of assuming tracklets are
accepted. For counting, require stable track IDs, a defined crossing/zone event, lifecycle policy,
and per-track count-once state; never count frame detections as unique objects.

## Verify representative behavior

Run the smallest representative fixture through the source and integrated paths. Use
`luxonis-inspect-pipeline` to show:

- Model input/crop matches the archive contract and intended scene region.
- Parsed labels/values match expected semantics.
- Detection, crop, track, depth, or secondary-result association remains correct.
- The intended downstream application state/output receives the model result.

Without replay or a device, run imports, syntax/config parsing, archive validation, source
inference when available, and deterministic host-logic tests. End
**code-integrated-awaiting-runtime** and list every pending hardware claim.

Report changed files, archive path/checksum, exact run command, evidence, passing contract checks,
and pending checks. Return to the calling build for the remainder of the vertical slice.
