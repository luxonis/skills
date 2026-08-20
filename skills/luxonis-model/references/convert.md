# Convert a custom model

Produce a target-platform NN Archive from an approved source. Retrieve the current
ModelConverter / HubAI path from MCP `luxonis__code`; do not reuse remembered flags.

## Path

Prefer the current HubAI path when the user authorizes upload. Use current ModelConverter when
local conversion is required and target prerequisites are available.

Use a dedicated conversion environment and record Python, DepthAI, converter, and related
versions. Accept a valid source NN Archive when available. Otherwise build configuration from
real model input, output, and preprocessing metadata. Verify that the selected converter
currently accepts the source format and operators.

Default to the current FP16 path when the backend exposes that mode. Use INT8 only for a
stated size, latency, power, or throughput need, with approved representative calibration
data and verified current parameter names. Re-evaluate after quantization.

If the source came from LuxonisTrain, start from its exported artifact. Do not copy training
callbacks, epochs, or dataset gates into conversion.

A checkpoint, raw ONNX, legacy blob, DLC without a matching contract, or compiler output is
not the requested archive.

## Validate

Run `scripts/validate_nn_archive.py` in an environment with matching DepthAI v3. Assert the
expected input dimensions, head/parser, and labels from the source contract.

Then compare source and converted inference on representative inputs when a supported adapter
is available: identical inputs and preprocessing, expected output structure, and appropriate
numeric or task-level similarity. After INT8, run the approved held-out comparison.

If converted inference requires integration or the target device, record the exact missing
runtime test and continue to integrate when that is how the evidence will be obtained. Do not
treat a successful conversion process or metadata gate as proof of useful inference.

Retry an unchanged failure no more than twice without a new hypothesis. On-device
benchmarking only when this session has a stated target-device performance requirement.
