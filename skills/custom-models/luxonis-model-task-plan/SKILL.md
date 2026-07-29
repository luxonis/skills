---
name: luxonis-model-task-plan
description: "Decompose an OAK model request and approve its staged model specification."
disable-model-invocation: true
argument-hint: "model request or project brief"
metadata:
  author: luxonis
  version: "1.0.0"
  status: experimental
---

# Luxonis Model Task Plan

Turn an ambiguous model request into an approved stage-by-stage specification. Read
`PROJECT_BRIEF.md` when present. Do not assume a sibling custom-model skill is installed.

End in exactly one state:

- **approved** -- the written specification is complete and the user approved it.
- **no-training-needed** -- Zoo search covers every requested stage; record the reusable models.
- **blocked** -- the request, Zoo, credentials, or required evidence prevents a sound plan.

<critical>
- Search the Zoo before proposing training for every stage. A suitable existing model is a
  legitimate successful outcome, not a failure. Record exact slugs, versions, input sizes,
  platforms, parsers, and semantic label order.
- Preserve task decomposition: classification is not detection, and detect-then-classify is not
  a two-class detector. Keypoints and segmentation require geometry-specific labels.
- Counting requires stable track IDs, an explicit crossing/zone event, and per-track count-once
  state. Use `neural-networks/counting/cumulative-object-counting` as the reference.
- Ask for approval after writing the specification. Do not start data work or training first.
</critical>

## 1. Read the request

Extract objects, attributes, actions, input surface, output surface, platform, latency, scene,
and acceptance metric. Read local `PROJECT_BRIEF.md` rather than asking again.

## 2. Decompose the pipeline

Choose explicitly among whole-frame classification, detection, detect-then-classify,
keypoints, segmentation, tracking, and counting. For each stage record:

- input and output;
- model task and class/keypoint names in order;
- crop or framing contract;
- platform and input size;
- acceptance metric and threshold;
- runtime association and visualization behavior.

## 3. Search the Zoo

Start with live docs from `https://docs.luxonis.com/llms.txt`, then use the installed CLI or SDK:

```bash
hubai model ls
hubai model info <slug>
```

Verify the CLI help and installed SDK when signatures differ. Search the task's synonyms,
adjacent tasks, and stages that could be split differently. Record why each stage is reused
or custom-trained. Check the installed `depthai-nodes` parser and output message before
declaring a custom parser necessary.

If `HUBAI_API_KEY` is absent, ask the user to provide it through the process environment. Do
not fabricate Zoo results; treat unavailable Zoo access as **blocked** rather than assuming no
reusable model exists.

## 4. Data and archive plan

If training remains necessary, name candidate datasets, object/instance counts, annotation
order, skeleton, visibility, license, download result, and exact Luxonis ML parser. Require
deployment-domain and runtime-framing validation. Define the LDF `instance_id`, normalized
keypoint triplets, and explicit skeleton metadata before dataset work.

## 5. Approval gate

Write the specification to the agreed project location and ask the user to approve it. If the
Zoo already solves the request, end **no-training-needed** and route to `luxonis-build-poc`.
Otherwise end **approved** only after approval. If a class is unavailable, surface the proposed
substitution and wait for approval rather than silently remapping it.

## Docs

- Docs source map -- https://docs.luxonis.com/llms.txt
- Model Zoo -- https://models.luxonis.com
- Luxonis ML -- https://github.com/luxonis/luxonis-ml
- Counting reference -- https://github.com/luxonis/oak-examples/tree/main/neural-networks/counting/cumulative-object-counting
