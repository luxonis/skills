---
name: luxonis-dataset-prepare
description: "Acquire, validate, and prepare a Luxonis Dataset Format training dataset."
disable-model-invocation: true
argument-hint: "approved task specification and dataset source"
metadata:
  author: luxonis
  version: "1.0.0"
  status: experimental
---

# Luxonis Dataset Prepare

Prepare an accepted Luxonis Dataset Format dataset from an approved task specification. Read
`PROJECT_BRIEF.md` when present. Do not assume a sibling custom-model skill is installed.

End in exactly one state:

- **dataset-ready** -- source, labels, framing, splits, health, and metadata pass all gates.
- **source-decision-needed** -- candidate access, labels, class substitutions, or framing need
  user approval.
- **blocked** -- the data cannot be made valid with the available evidence.

<critical>
- Use a dedicated virtual environment and verify the installed `luxonis-ml` version.
- For `clsdir`, use `train/valid/test`; `val` can silently omit validation. Always pass an
  explicit `--task-name`.
- Hash all content globally before splitting. Persist class order with explicit
  `set_classes(..., rewrite_metadata=True)` and assert it, because archive labels inherit it.
- Folder labels do not prove whole-object framing. Match source imagery to detector/cropper
  framing at runtime before accepting it.
- Surface unavailable approved classes and obtain substitution approval. Never silently swap.
</critical>

## 1. Select and score sources

Score at least two candidates for dog/object count, annotation semantics/order, skeleton,
visibility, license, parser support, domain fit, and actual downloadability. Attempt the top
candidate and record the exact URL/command and result. Do not claim access from a landing page.

Use only live Luxonis docs starting at `https://docs.luxonis.com/llms.txt` for current parser
facts. Check `luxonis_ml.enums.DatasetType` in the active environment. Common keypoint formats
are `COCO`, `YOLOV8KEYPOINTS`, and `ULTRALYTICSNDJSONKEYPOINTS`; unsupported source JSON needs a
custom LDF generator.

## 2. Validate domain and annotations

Check that images depict the complete object at the deployment scale and aspect ratio. If
folder labels or source framing fail, run a CPU detector over every candidate image:

- keep exactly one confident target detection;
- choose confidence and box-area thresholds empirically and record the evidence;
- require a minimum detector-box area and per-class survivor gate;
- crop the box with a recorded margin so training framing matches `FrameCropper`;
- record detector name, version, license, thresholds, margin, and per-class keep rates.

Reject or surface sources with too few survivors. Keep a held-out deployment-domain set.

## 3. Parse and enforce metadata

Use the installed parser with an explicit task name. For keypoints, ensure every instance has
normalized `(x, y, visibility)` triplets, COCO visibility `0` not labeled, `1` occluded, `2`
visible, and a shared `instance_id` for its box and keypoints. Set semantic labels and 0-based
skeleton edges explicitly.

For classification, count files directly by split and class because `get_statistics()` in
some installed `luxonis-ml 0.9.0` builds does not expose classification distributions. Verify
Parquet/split counts directly. Use `valid`, not `val`.

## 4. Deduplicate, split, and gate

Globally SHA-256 hash before assigning splits. Remove cross-split duplicates, then rebalance to
the approved class order without silently shrinking below a usable minimum. Run health checks,
per-class/per-split counts, label spot checks, and metadata assertions. Record source terms,
parser, task, class order, hashes, framing gate, curation settings, and final counts.

If a sibling training skill is unavailable, stop at **dataset-ready** with the exact accepted
LDF path and use the Docs links for the next stage.

## Docs

- Docs source map -- https://docs.luxonis.com/llms.txt
- Luxonis ML -- https://github.com/luxonis/luxonis-ml
- [Dataset parsing tutorial](https://github.com/luxonis/ai-tutorials/blob/main/training/dataset-preparation/dataset_parsing.ipynb)
- [Custom dataset generator](https://github.com/luxonis/ai-tutorials/blob/main/training/dataset-preparation/custom_dataset_generator.ipynb)
