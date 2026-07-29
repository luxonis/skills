---
name: luxonis-custom-model-app
description: "Route and run a gated custom-model workflow for a Luxonis OAK application."
disable-model-invocation: true
argument-hint: "model or application goal"
metadata:
  author: luxonis
  version: "1.0.0"
  status: experimental
---

# Luxonis Custom Model App

Use this skill when the Model Zoo does not fully serve the requested application and a
custom-model workflow may be needed. Read `PROJECT_BRIEF.md` in the current directory when it
exists. Do not assume a sibling custom-model skill is installed -- if one is unavailable,
perform that stage's documented checks inline or stop with its named blocker.

End in exactly one state:

- **no-training-needed** -- Zoo models cover the approved stages; record the reuse decision and
  route to `luxonis-build-poc`.
- **spec-awaiting-approval** -- write the decomposition and stop for user approval.
- **archive-ready** -- accepted data, evaluation, and a validated target-platform archive exist.
- **app-ready** -- a standalone app exists with the claimed validation evidence.
- **blocked** -- one stage cannot proceed; report evidence and the next action.

<critical>
- Search the Model Zoo before proposing training. Do not train what an acceptable public model
  already solves. The dog-pose reconnaissance is the calibration case: SuperAnimal plus the
  animal-pose example made training unnecessary.
- Do not train before the written task specification is approved.
- Keep training/data and app-runtime tools in separate virtual environments.
- Do not claim hardware success from host checks, and do not claim counting from per-frame
  detections.
</critical>

## 1. Preflight

Read the user request and `PROJECT_BRIEF.md` if present. Treat `PROJECT_BRIEF.md` as the
workflow marker and source of truth for the target platform, app surface, acceptance threshold,
and constraints. Use it instead of re-interviewing. Keep stage artifacts and evidence beside
the project, but do not replace the shared marker convention with a custom `run-state.md`.

## 2. Route the stages

1. Run `luxonis-model-task-plan` first. Search the Zoo for every stage.
2. If all stages have acceptable Zoo models, end **no-training-needed** and route to
   `luxonis-build-poc`.
3. After approval, run `luxonis-dataset-prepare` and stop at its health, balance, framing,
   deduplication, and label-order gate.
4. Run `luxonis-model-train` and stop at its evaluation and archive gate.
5. Run `luxonis-model-integrate` and report host, replay, and device evidence separately.

When a sibling skill is unavailable, preserve the same gate and use the relevant Docs links;
do not silently skip it.

## 3. Cross-stage rules

- Keep approved class names and order fixed from plan through archive and app labels.
- Surface unavailable classes and obtain substitution approval before changing labels.
- For counting, require stable track IDs, an explicit crossing or zone event, and per-track
  count-once state. Use `neural-networks/counting/cumulative-object-counting` as a reference
  after cloning oak-examples into `~/.luxonis/agent-context/`.
- Use no-device fallback checks only as described by the integration skill, and list pipeline,
  replay, association, packaging, and RVC4 execution as pending.

## Docs

- Docs source map -- https://docs.luxonis.com/llms.txt
- Model Zoo -- https://docs.luxonis.com/software-v3/ai-hub/
- OAK examples -- https://github.com/luxonis/oak-examples
- Custom model training -- https://github.com/luxonis/ai-tutorials
