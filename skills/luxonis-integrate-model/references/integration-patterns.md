# Model integration patterns

Read only the section matching the archive task. Verify all exact APIs with current Luxonis source.

## Single-stage classification, detection, segmentation, or pose

- Drive input and preprocessing from archive metadata.
- Preserve parser/head and label/keypoint order.
- Inspect representative input plus parsed output and mapped overlay/state.

## Detect then classify, recognize, read, or estimate keypoints

- Derive crops from the same filtered detections used by dependent tracking/state.
- Prefer original-frame information when the secondary model needs detail lost at detector input.
- Verify crop framing/aspect ratio against the secondary archive contract.
- Preserve association through timestamps or a currently supported verified gather mechanism.
- Inspect detections, crops, secondary output, and final association.

## Tracking, counting, zones, and dwell

- Treat tracker lifecycle states explicitly.
- Define entry, crossing, zone, dwell, or disappearance semantics.
- Count one event per stable track ID according to the policy, not one detection per frame.
- Test lost/reappearing and boundary cases on a bounded sequence.

## Depth or spatial association

- Verify alignment target, coordinate frame, units, invalid-depth policy, and ROI aggregation.
- Associate depth and detections from synchronized lineage.
- Inspect representative aligned image/depth and structured spatial output.

## Multi-input or custom-output archives

- Match every named input/output and dtype/layout from the archive.
- Verify synchronization and data lineage before application logic.
- When archive metadata lacks required postprocessing, stop for an explicit parser/interface
  decision rather than guessing raw tensor semantics.
