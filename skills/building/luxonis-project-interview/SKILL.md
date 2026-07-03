---
name: luxonis-project-interview
description: "Interview the user and produce a buildable Luxonis project brief."
disable-model-invocation: true
argument-hint: "project idea or application goal"
metadata:
  author: luxonis
  version: "1.0.0"
  status: stable
---

# Luxonis Project Interview

Produce a **buildable brief**: a plain-language project spec in `PROJECT_BRIEF.md`
that a later Luxonis build session can use.

Completion is not a running app. Completion is:

1. `PROJECT_BRIEF.md` written in the agent's current working directory.
2. The user asked to review it.

Keep the interview product/application-level. Assume this may be the user's first
Luxonis interaction.

## Rules

- Ask **one question at a time**.
- For each question, say why it matters and give a recommended/default answer when useful.
- Do not ask about DepthAI, nodes, pipelines, RVC, model conversion, queue settings,
  `oakctl`, Hub, or OAK app internals.
- If local files or Luxonis docs answer a factual question, use them instead of asking.
- Accept `unknown` / `not sure yet`, but push once for a rough answer first.
- Ask only the next question needed to make the brief buildable.
- Do not edit files in `$PWD` except `PROJECT_BRIEF.md`.

## 1. Preflight

Before interviewing, inspect only the current working directory. List it, then read any of
these that are present:

- `PROJECT_BRIEF.md`
- `DEVICE.md`
- `README.md`
- obvious project manifests such as `pyproject.toml`, `requirements.txt`, `package.json`
- obvious source/example files

Do **not** read `AGENTS.md` or `CLAUDE.md` as interview source material. They are agent
guidance, not customer project facts.

If an initial idea was passed to the skill, summarize it in one sentence and treat inferred
fields as tentative.

If `PROJECT_BRIEF.md` already exists:

- Summarize what it says.
- If the user is continuing the same project, update it in place.
- If this is a different project idea, stop and tell the user to run the skill from a
  dedicated/different folder.

If `DEVICE.md` exists, use it for device facts. If not, ask for the device in plain language.
If the user does not have a device yet, continue and record that as an assumption.

## 2. Interview spine

Drive toward these required fields. Skip any already answered by preflight or the user's
initial idea.

1. **Device availability** -- "Which Luxonis camera/device do you have for the first demo? If
   you don't have one yet, say `not yet`."
2. **Desired run location** -- "For the first demo, should this run on your laptop/computer
   connected to the camera, on a small on-site computer, directly on the camera without a
   computer connected, or are you not sure yet?"
3. **Real-world goal** -- "What should this help someone do or decide in the real world?"
4. **One primary demo behavior** -- detect/classify, count, track movement, measure, read
   text/codes, guide navigation, save evidence, or another single behavior.
5. **Targets / events** -- exact objects, people, actions, states, or events, using the
   customer's words.
6. **First scene** -- where the camera is placed, what is in view, rough distance, and what
   makes the scene difficult.
7. **Outputs / actions** -- what the user sees, saves, receives, or triggers when it works.
8. **Success criteria** -- observable demo checks, not ML metrics unless the user provides
   them.
9. **Sample media / replay** -- whether photos, video, or a short real-scene recording can be
   captured for implementation and verification.
10. **First demo vs later** -- the smallest demo that proves value, and what belongs later.

Use plain examples only when the user is stuck. Example primary behaviors:

- count people entering an area
- detect a worker in a restricted zone
- measure object position or distance
- read labels, text, or codes
- guide a robot around obstacles
- save an image or event when something happens

For desired run location, do not teach platform terms. Internally remember: some devices need
a connected computer/server, while some can support camera-only operation. If the user wants
camera-only operation, record an assumption that future work must confirm the selected device
supports it.

**Draft gate:** write the first draft once every spine field is answered or explicitly marked
unknown/assumed. Do not keep interviewing past that point; conditional probes are added only
when they materially affect the first demo.

## 3. Conditional probes

Do not turn the interview into a full consulting checklist. Ask these only when they materially
affect the first demo or feasibility.

- **False alarms** -- if targets are ambiguous: "What should it ignore, even if it looks
  similar?"
- **Privacy** -- if people, faces, license plates, private areas, or sensitive footage may be
  visible.
- **Internet/offline** -- if cloud services, model downloads, remote dashboards, or offline use
  are mentioned.
- **Zones/lines/regions** -- if counting, safety, measurement, shelves, doorways, paths, or
  alerts depend on a physical area in the image.
- **One camera vs multiple views** -- if the scene cannot be covered by one camera.
- **Operator interaction** -- if the demo may need someone to click/select/configure a target,
  region, threshold, or recording.
- **Integrations** -- only after the core demo behavior is clear.
- **Audience** -- if who judges the demo changes the output, action, or success criteria.
- **Timeline** -- if scope pressure matters.
- **Common vs site-specific target** -- if recognition feasibility is unclear: "Are these common
  everyday things, or specific to your business/site/product/process?"
- **Approximation** -- if the target sounds site-specific or specialized: "For the first demo, is
  a rough stand-in target acceptable?" (Example/model readiness is checked post-brief, so judge
  this from how the user describes the target, not from a model search.)

If the target appears site-specific, record that dataset collection and model training may be
needed. Do not claim the agent can train a model in this workflow.

## 4. Keep alignment visible

After important corrections or several answers, give one compact running-understanding line:

> Captured so far: laptop-connected demo, people counting at a store entrance, live view plus
> event log. Next missing piece: success criteria.

Only show a remaining-field checklist when it helps orientation, for example when the user asks
"what else?" or the interview is getting long.

## 5. Write the brief

Write to exactly:

```text
$PWD/PROJECT_BRIEF.md
```

Do not search for a Git root. Do not write the brief to `~/.luxonis/agent-context/`. Do not
create scripts, app code, `DEVICE.md`, `AGENTS.md`, or `CLAUDE.md`.

Infer a short descriptive title for the `# Project Brief:` heading from the goal. Do not ask
the user to name the project unless they want naming/branding.

Use this template. Keep it concise. If a section is not known, write `Not specified yet.` and
capture the assumption or open question.

```md
# Project Brief: <short descriptive title>

## Goal

## Device

## Desired run location

## Target user / demo audience

## First demo scope

## Later / out of scope

## Scene

## Targets / events

## Outputs / actions

## Success criteria

## Sample media / replay

## Constraints

## Assumptions and open questions
```

This file is a **pure project spec**. Do not include a suggested implementation path, example
recommendations, model names, or Luxonis technical architecture unless the user explicitly asks
to add them.

After writing, say:

> Please review `PROJECT_BRIEF.md`. Tell me what is wrong or missing and I'll patch it.

Patch only the relevant sections. Do not restart the whole interview unless the correction
changes the core project.

## 6. Optional post-brief example/model readiness

Only after `PROJECT_BRIEF.md` is written, optionally look for existing Luxonis baselines. This
has zero effect on whether the brief is complete.

Use `~/.luxonis/agent-context/oak-examples` as the local reference checkout, sourced the safe
way:

- Create the directory `~/.luxonis/agent-context` (in the user's home) if it does not exist.
- Clone `https://github.com/luxonis/oak-examples` over **HTTPS** (never SSH), shallow and
  pinned to `main` (which tracks DepthAI v3), with git's low-speed guard
  (`http.lowSpeedLimit=1000`, `http.lowSpeedTime=60`) so a stalled network aborts instead of
  hanging. Clone into a temporary sibling path (e.g. `oak-examples.tmp`) and rename it into
  place only on success, using commands appropriate to the host shell, so a failed clone never
  leaves a partial checkout behind. If the checkout already exists, refresh it with a
  fast-forward-only pull instead.
- A checkout is usable only if it contains `INDEX.md`. If the clone fails or is incomplete,
  report the short reason and continue -- the brief is already complete; never rely on a partial
  checkout or older/v2 examples.

To recommend an example:

1. Use `INDEX.md` to find candidates.
2. Read the selected example's `AGENTS.md`.
3. Read its `README.md` when run instructions or details are needed.
4. Describe only what those files support:
   - what the example does
   - what it does not do
   - output / success looks like
   - whether it is a close match or only a nearby baseline

Also use Luxonis docs via `https://docs.luxonis.com/llms.txt` when checking whether a Model Zoo
model or documented pattern likely exists.

Report one readiness tier in chat, not in the brief unless the user asks:

- **Ready baseline likely exists** -- close OAK example and/or Model Zoo model.
- **Approximate demo possible** -- nearby example/model, but not exact target.
- **Dataset/training likely needed** -- no obvious existing example/model fit.

If dataset/training is likely needed, recommend sample capture and model/data requirements; do
not claim to train the model.

## 7. Optional zero-build example run

If a close existing example exists, describe it accurately first, then ask one question:

> I found a close existing example. Do you want me to try running it on your device now?

Only attempt this if device context is verified by `DEVICE.md`. A device the user merely named
during the interview is not verified; if there is no `DEVICE.md`, recommend `luxonis-device-setup`
instead.

Run policy if the user agrees:

- Use the example's documented command.
- Prefer script/peripheral mode when available.
- Install dependencies only in an isolated local environment; no global Python packages.
- Do not flash, adopt, factory reset, or persistently install/deploy anything to the camera
  unless explicitly approved.
- Standalone/OAK-app runs are allowed when appropriate, but explain any persistent action before
  doing it.

A failed example run does not invalidate the interview. The skill was complete when
`PROJECT_BRIEF.md` was written and review was requested.

## 8. End with the next step

End with the shortest useful next step:

- No verified device / no `DEVICE.md`: recommend `luxonis-device-setup`.
- Brief written and device ready: recommend `luxonis-build-poc`.
- Close zero-build example exists: offer that run first; use `luxonis-build-poc` for custom work.
