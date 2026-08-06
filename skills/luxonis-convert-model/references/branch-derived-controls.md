# Branch-derived conversion controls

These controls were retained from experimental custom-model branch commit
`d455d573aa7f9ef4d96753f060f9e77859441b80`. They are technical baselines, not permission to run
the branch's training workflow. Confirm names against the installed/current converter schema.

## Environment and authentication

- Use a dedicated conversion environment and record package/CLI versions.
- Set `HUBAI_API_KEY` only in the process environment.
- Treat a keyring warning as benign only when environment authentication actually succeeds.
- Keep conversion, training, and app-runtime environments separate when they already exist.

## Precision baseline

The branch defaulted to `FP16_STANDARD`. For an explicit INT8 requirement it used representative
`quantization_data` and `max_quantization_images`. Map that intent into the current supported
ModelConverter/HubAI interface; do not paste training exporter YAML into another API.

INT8 requires:

- A stated resource/performance reason.
- Approved representative calibration data.
- Current verified parameter names.
- Post-conversion held-out comparison.

## Archive gate retained from the branch

Before integration, require:

1. A real target-platform NN Archive, not only a checkpoint, ONNX file, legacy blob, or compiler
   output.
2. Input dimensions, parser/head metadata, and approved class/keypoint order validated with
   `scripts/validate_nn_archive.py`.
3. Representative source-versus-converted inference.
4. Post-conversion comparison after INT8.
5. A named failure stage after at most two unchanged retries.

Do not carry forward LuxonisTrain callbacks, epochs, metrics, dataset gates, or training
remediation. V2 starts from an approved exported artifact.
