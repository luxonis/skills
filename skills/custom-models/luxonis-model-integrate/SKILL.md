---
name: luxonis-model-integrate
description: "Integrate a validated custom NN Archive into a standalone Luxonis OAK application."
disable-model-invocation: true
argument-hint: "validated archive and approved application brief"
metadata:
  author: luxonis
  version: "1.0.0"
  status: experimental
---

# Luxonis Model Integrate

Build a standalone app only after archive acceptance. Read `PROJECT_BRIEF.md` when present.
Do not assume a sibling custom-model skill is installed.

End in exactly one state:

- **app-ready** -- standalone app exists and the claimed host/replay/device evidence is recorded.
- **blocked** -- an archive, dependency, example, replay, or device prevents the requested
  validation.

<critical>
- Read live Luxonis docs from `https://docs.luxonis.com/llms.txt` and clone references into
  `~/.luxonis/agent-context/`; never assume this repo is an oak-examples checkout.
- Read `INDEX.md` in the shallow HTTPS `main` checkout before choosing an example. Bootstrap a
  standalone copy outside the checkout and never edit the reference checkout.
- Verify that `FrameCropper.fromImgDetections()` takes `ImgDetections`, not `Tracklets`.
- Feed the same filtered detector stream to tracker and cropper. Tracker label filtering does
  not filter the detector stream consumed by the cropper.
- Do not claim stable tracker-label association from timestamp/order joining until replay or
  hardware validates it.
- Without a device, use the no-device tier and list hardware claims as pending.
</critical>

## 1. Preflight and references

Read `PROJECT_BRIEF.md`, archive validation, class/keypoint order, target mode, and device marker
if present. Use a dedicated app-runtime virtual environment. Clone references lazily and safely:

```bash
mkdir -p ~/.luxonis/agent-context
# shallow HTTPS clone of https://github.com/luxonis/oak-examples, branch main,
# with http.lowSpeedLimit=1000 and http.lowSpeedTime=60; clone to a temporary sibling,
# then rename only after INDEX.md exists
```

Read `INDEX.md`, `ESSENTIAL_KNOWLEDGE.md`, the closest example's `AGENTS.md`, and `README.md`.
Keep paths such as `neural-networks/counting/cumulative-object-counting` as reference paths,
not as assumptions about the current checkout. If the bootstrap helper is unavailable, copy the
selected example manually while preserving its runtime shape and removing source-only guidance.

## 2. Build the smallest graph

For detect-then-classify, preserve detector -> `FrameCropper.fromImgDetections` -> classifier
`ParsingNeuralNetwork` -> `GatherData` -> annotation. Use archive input dimensions. For tracking,
filter detections before both `ObjectTracker` and `FrameCropper`, assert equal item counts, and
handle NEW/TRACKED/LOST/REMOVED explicitly. Counting requires track IDs, a crossing/zone event,
and per-track count-once state -- never count detections per frame.

Inspect archive metadata rather than hard-coding labels or skeleton edges. Rewrite generated
`AGENTS.md` and `CLAUDE.md`; bootstrap copies the source example's files verbatim.

## 3. Verify honestly

With hardware or replay, verify frames, detector/crops, parser labels, association, output, and
counting events. Without both, run only:

- Python imports and compile/syntax checks;
- TOML/config parsing;
- NN Archive validation with expected metadata/order;
- ONNX Runtime smoke inference on held-out crops when an ONNX export exists;
- synthetic host tests for voting, minimum crop, low-confidence rejection, track lifecycle, and
  count-once crossing.

Record pipeline start, replay, tracker continuity, classifier-to-track association, standalone
packaging, and RVC4 execution as pending when they were not run. Do not call host checks
on-device validation.

## Docs

- Docs source map -- https://docs.luxonis.com/llms.txt
- DepthAI v3 -- https://docs.luxonis.com/software-v3/depthai/
- OAK apps -- https://docs.luxonis.com/software-v3/oak-apps/
- `oakapp.toml` -- https://docs.luxonis.com/software-v3/oak-apps/configuration.md
- OAK examples -- https://github.com/luxonis/oak-examples
