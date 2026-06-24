---
name: luxonis-build-poc
description: "Build a thin runnable Luxonis proof of concept from a project brief."
disable-model-invocation: true
argument-hint: "project brief path or application goal"
metadata:
  author: luxonis
  version: "0.1.0"
  status: placeholder
---

# Luxonis Build POC

This is a placeholder skill.

Eventually, this skill should build a **thin POC** from a project brief: the smallest runnable Luxonis/OAK application that demonstrates the core value without pretending to be production-ready.

The final skill should strongly prefer adapting known-good Luxonis examples over inventing APIs from memory.

## Intended job

The final skill should guide the agent to:

1. Find or create the project brief.
2. Identify the closest OAK example or documented pattern.
3. Choose the simplest viable implementation path.
4. Build one vertical slice that runs.
5. Verify it with a concrete run command.
6. Document assumptions, gaps, and next steps.

## Matt examples to study

- [`tdd`](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) for vertical slices, tracer bullets, and avoiding horizontal overbuild.
- [`to-prd`](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-prd/SKILL.md) for turning conversation context into a durable implementation artifact.
- [`codebase-design`](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md) for simple interfaces and testable seams.
- [`writing-great-skills`](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md) for completion criteria and pruning.

## Waiting for user input

Before writing the real skill, ask for input on:

1. What counts as a Luxonis POC for phase one.
2. Preferred project types: OAK App, host-side Python script, peripheral mode, or other.
3. Which repositories/docs/examples the agent should use first.
4. Guardrails for common bad behavior: hallucinated APIs, V2/V3 confusion, unnecessary custom DepthAI builds, over-engineering.
5. How the skill should behave if no project brief exists.

Do not invent the build workflow yet.
