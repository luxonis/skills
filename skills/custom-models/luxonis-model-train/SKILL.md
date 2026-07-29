---
name: luxonis-model-train
description: "Train and convert an approved Luxonis model into a validated platform NN Archive."
disable-model-invocation: true
argument-hint: "accepted LDF dataset and approved model specification"
metadata:
  author: luxonis
  version: "1.0.0"
  status: experimental
---

# Luxonis Model Train

Train only after dataset acceptance and user approval. Read `PROJECT_BRIEF.md` when present.
Do not assume a sibling custom-model skill is installed.

End in exactly one state:

- **archive-ready** -- evaluation passes, archive metadata is correct, and the target archive is
  validated.
- **blocked** -- training, conversion, evaluation, or archive validation cannot proceed.

<critical>
- Use a dedicated training virtual environment and verify installed package versions.
- Enable at least one tracker integration. All three disabled raises
  `ValueError: At least one integration must be used!`.
- Inspect resolved config and callbacks before training. `smart_cfg_auto_populate` may add
  `UploadCheckpoint`, `TestOnTrainEnd`, and `ConvertOnTrainEnd`.
- Measure one CPU epoch first and separate training/export time from HubAI conversion time.
- Default to `FP16_STANDARD`. Use INT8 only for a stated latency/size/throughput requirement,
  with verified `quantization_data` and `max_quantization_images`, then re-evaluate the
  converted archive.
- Never put `HUBAI_API_KEY` in YAML or logs. A keyring warning is benign when environment
  authentication succeeds.
</critical>

## 1. Configure

Select the predefined family and verified variant, including `KeypointDetectionModel` for
instance keypoints. Start from the installed config/schema, not memory. Keep approved class or
keypoint order unchanged. Configure HubAI conversion with the target platform and
`FP16_STANDARD`; set `HUBAI_API_KEY` only in the process environment.

Default exporter configuration:

```yaml
exporter:
  quantization_mode: FP16_STANDARD
  hubai:
    active: true
    platform: rvc4
    params: {}
    delete_remote_model: false
```

For INT8, use only verified HubAI keys:

```yaml
exporter:
  quantization_mode: INT8_STANDARD
  hubai:
    active: true
    platform: rvc4
    params:
      quantization_data: /absolute/path/calibration.zip
      max_quantization_images: 200
```

## 2. Resolve and time

Load the config through the installed schema. Record preprocessing, loader, exporter, metric
task, integrations, and final callback list. Verify classification metrics resolve to
multiclass instead of accepting an unexplained inference warning. Run a one-epoch CPU timing
trial, noting that it may export an ONNX archive even with HubAI inactive. Project the full run
before committing to its epoch budget.

Use this timing command for the trial:

```bash
luxonis_train train --config ./timing-config.yaml
```

## 3. Train and evaluate

Run the approved training command:

```bash
luxonis_train train --config ./config.yaml
```

Report real test metrics, per-class metrics, and a confusion
matrix when available. State whether `TestOnTrainEnd` or a separate test command produced them
and which checkpoint/model state they evaluate. Do not tune to chase a PoC number; stop and
escalate if results are near chance or violate the approved gate.

## 4. Convert and validate

Confirm ONNX and host archive artifacts, then obtain the target-platform archive via
`exporter.hubai` and `ConvertOnTrainEnd`. Validate it with this skill's
`scripts/validate_nn_archive.py`, asserting input size, parser/head metadata, and approved
labels in order. For INT8, run post-conversion held-out evaluation and compare it to the
approved threshold. A checkpoint, ONNX file, or legacy blob alone is not deployable.

If conversion fails, preserve the exact stage and error and retry no more than twice without a
new decision. If a sibling integration skill is unavailable, stop at **archive-ready** and
report the standalone archive path and pending app work.

If `HUBAI_API_KEY` is absent, ask the user to provide it through the process environment and
stop **blocked** before conversion. Never fabricate Zoo or conversion results, and never place
the key in YAML or logs. Do not present a checkpoint-only result as an archive deliverable.

## 5. Bounded remediation

If the approved metric misses its threshold, make at most three bounded attempts: audit or
rebalance data, adjust verified preprocessing/augmentation, or change the approved variant or
epoch budget. After the third miss, stop for a quality, threshold, or model decision. Do not
silently lower the threshold or tune indefinitely.

## Docs

- Docs source map -- https://docs.luxonis.com/llms.txt
- LuxonisTrain -- https://github.com/luxonis/luxonis-train
- LuxonisTrain configs -- https://github.com/luxonis/luxonis-train/tree/main/configs
- Training tutorial -- https://github.com/luxonis/ai-tutorials/blob/main/training/train_classification_model.ipynb
