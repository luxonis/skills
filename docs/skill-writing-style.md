# Skill writing style

This repo should follow a Matt Pocock-inspired skill style: compact, precise, and designed to produce predictable agent behavior.

## Core rules

- Prefer short skills over comprehensive manuals.
- Give the agent a process, not a lecture.
- Use strong leading words that shape behavior: `device-ready`, `thin POC`, `known-good example`, `tight loop`, `support packet`.
- Every workflow skill needs a completion criterion.
- Ask one question at a time when interviewing the user.
- Do not bury critical constraints in the middle of a long file.
- Move detailed reference material behind context pointers in `references/` only when it is needed.
- Delete no-op advice. If a line would not change agent behavior, cut it.

## Manual-only descriptions

All Luxonis skills are user-invoked only. Because of that, frontmatter descriptions are human-facing labels, not model-trigger prompts.

Good:

```yaml
description: "Bring a Luxonis OAK camera to a verified device-ready state."
```

Avoid:

```yaml
description: "Use when the user mentions OAK, USB, PoE, device discovery, troubleshooting..."
```

Trigger phrases are wasted when `disable-model-invocation: true` is set.

## References to emulate

- Matt's [`writing-great-skills`](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md): vocabulary for predictability, information hierarchy, pruning, leading words.
- Matt's [`ask-matt`](https://github.com/mattpocock/skills/blob/main/skills/engineering/ask-matt/SKILL.md): router skill structure.
- Matt's [`grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md): one-question-at-a-time interview loop.
- Matt's [`grill-with-docs`](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md): user-invoked wrapper over a sharper interview/documentation discipline.
- Matt's [`diagnosing-bugs`](https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnosing-bugs/SKILL.md): disciplined diagnosis loop and tight feedback loop.
- Matt's [`tdd`](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md): vertical slices and tracer bullets.

## How to replace a placeholder

When turning a placeholder into a real skill:

1. Start from real Luxonis source material: docs, support tickets, known failure modes, benchmark transcripts, OAK examples, app team feedback.
2. Define the leading word for the skill.
3. Define the completion criterion.
4. Write the smallest workflow that gets the agent to that criterion.
5. Add guardrails for the most likely bad agent behavior.
6. Add only the references needed by the workflow.
7. Test manually against a realistic scenario before adding more detail.

## Anti-goals

- Do not create huge runbooks.
- Do not split into many tiny one-off skills yet.
- Do not add scripts until we see agents repeatedly reinventing the same command.
- Do not let the agent clone or build large Luxonis repositories unless the workflow explicitly needs it.
- Do not invent support escalation rules without support-team input.
