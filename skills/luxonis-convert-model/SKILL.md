---
name: luxonis-convert-model
description: Convert an approved customer-provided or public ONNX, TFLite, OpenVINO IR, source NN Archive, or supported model artifact into a validated target-compatible Luxonis NN Archive for a named OAK/RVC platform. Use when an OAK application needs a model that is not already available in a compatible Luxonis format. Do not use to train a model, collect a dataset, choose an unapproved third-party license, or merely integrate an already-compatible archive.
---

# Luxonis Convert Model

Produce a validated integration contract and target-platform NN Archive from an approved source.
Use current ModelConverter, HubAI, NN Archive, and target documentation rather than remembered
commands.

End in one state:

- **archive-ready:** source and converted artifacts exist, metadata passes, and representative
  converted behavior matches the source or approved expected result with recorded evidence.
- **archive-metadata-valid-awaiting-inference:** the converted artifact and metadata pass, but no
  supported runtime is available for the required representative behavior check. The archive may
  enter integration to obtain that evidence, but is not yet archive-ready.
- **blocked:** source, target, license/upload approval, metadata, credentials, conversion, or
  validation prevents an integration-ready result.

## Establish the source contract

Use `POC_PLAN.md` and `MODEL_CONVERSION.md` when present, but do not require them. Require:

- Explicit target device and RVC platform.
- Explicit RVC2 or RVC4 target compatibility; executable formats and compiler paths are
  target-dependent, so retrieve the current mapping rather than reusing an artifact across them.
- Exact source artifact, immutable version/checksum, publisher, and accepted license.
- User approval of third-party weights/license and any cloud upload. Approval of the exact model
  revision and license may already be recorded in the reviewed `POC_PLAN.md`; do not ask again.
  Cloud upload always remains separately explicit.
- Task, input names/shapes/layouts/dtypes, color and preprocessing.
- Output names/shapes/semantics, heads/parser, and label/keypoint order.
- A small representative input set for comparison.

Inspect the graph and original publisher/inference code when metadata is missing. An ONNX file
alone is not a complete deployment contract. Stop rather than guess tensor semantics.

Use a dedicated conversion environment and record Python, DepthAI, ModelConverter, HubAI, and
related versions. Keep credentials such as `HUBAI_API_KEY` in the process environment only; never
place them in config, reports, displayed shell history, or logs.

Read `references/branch-derived-controls.md` and `references/conversion-gates.md` before running a
conversion.

## Select the current supported path

Retrieve live conversion docs through Luxonis MCP and verify installed CLI help. Prefer the
current supported HubAI/HubAI SDK path when the user authorizes upload. Use current ModelConverter
when local conversion is required and target prerequisites are available.

Accept a valid source NN Archive when available. Otherwise create its configuration from real
model input/output and preprocessing metadata. Verify that the selected converter currently
accepts the source format and operators. Record path, tool version, target, and why it was chosen.

## Preserve the complete model contract

Preserve:

- Input names, shapes, layout, dtype, image type, channel order, scale, and mean.
- Output names, shapes, task semantics, heads/parser, and postprocessing.
- Labels/keypoints in exact order.
- Source revision/checksum and license.

Default to the current FP16 standard path when the selected backend exposes the branch-derived
precision modes. Use INT8 only for a stated size, latency, power, or throughput requirement, with
approved representative calibration data and verified current parameter names. Re-evaluate after
quantization.

Do not copy training configuration, callbacks, epochs, or dataset gates into conversion. When the
source came from LuxonisTrain, start from its exported artifact and preserve export provenance.

## Convert and retain evidence

Run the exact current conversion command. Save redacted config/command, tool versions, target,
precision, timestamps, source checksum, logs, and output paths. Retry an unchanged failure no more
than twice without a new hypothesis.

A checkpoint, raw ONNX, legacy blob, DLC without a matching contract, compiler output, or
incomplete archive is not the requested integration-ready result.

## Validate before integration

Run `scripts/validate_nn_archive.py` in an environment with matching DepthAI v3. Assert the
expected input dimensions, head/parser, and labels from the source contract. This is a metadata
gate, not an accuracy test.

Then compare source and converted inference on representative inputs when a supported adapter is
available:

- Identical inputs and intended preprocessing.
- Expected output structure and semantic labels.
- Appropriate numeric or task-level similarity.
- Approved held-out quality gate after INT8.

If converted inference requires integration or the target device, end
**archive-metadata-valid-awaiting-inference** and record the exact missing runtime test. Only end
**archive-ready** after representative converted behavior matches the source or approved expected
result. A successful conversion process or metadata gate alone is not archive-ready.

Use current on-device benchmarking only when the POC has a stated target-device performance
requirement. A successful conversion process is not proof of useful inference or performance.

Write `MODEL_CONVERSION.md` from `assets/MODEL_CONVERSION.template.md`. Return the archive and
contract to `luxonis-integrate-model` or the calling build.
