# V2 Lightweight direction

## Status

Rough architectural draft for discussion. It has not been benchmarked or validated with customers
or representative device tasks and should not be treated as release-ready behavior.

## Capability step

V1 helps an engineer get an OAK connected and reach an example-level application. V2 Lightweight
aims to help that engineer produce a working proof of concept for their actual use case: reviewed
architecture, customer-specific behavior, repeatable execution, observable output, and explicit
limitations. The target is a credible demo, not production readiness or a claim that every
human-owned subsystem has been solved.

## Product split

Luxonis MCP and pipeline inspection are assumed parts of the next release:

- MCP provides current documentation, examples, device facts, and model context.
- Pipeline inspection exposes what a running DepthAI application actually produces.
- Skills add the durable workflow around those capabilities: choosing what to verify, planning
  only when material decisions exist, requiring human plan approval, iterating from evidence, and
  handing off unsupported subsystems cleanly.

This avoids copying broad DepthAI documentation into prompts. The model and its coding harness do
most of the engineering work; skills supply the Luxonis-specific constraints most likely to be
missed.

## Interaction model

`luxonis-build` is the normal entry point and a lightweight orchestrator. It dynamically gathers
missing use-case constraints, diagrams a new or materially changed pipeline, pauses for human
review, and then runs a build-inspect-fix loop. Narrow setup, inspection, troubleshooting,
conversion, and integration skills can be selected by the agent or invoked directly, so the
customer does not need to understand a prescribed sequence.

Model training, training-data programs, proprietary SLAM, full ROS systems, and productionization
remain outside this draft. Supported OAK work should continue behind a clear interface when one of
those subsystems must be completed by a human or a separate effort.

## Validation needed

Before merge, compare this branch against V1 and a no-skill baseline on representative OAK tasks.
Measure activation accuracy, question quality, plan correctness, time to first useful output,
device success, regressions, unnecessary context load, and whether another engineer can reproduce
the final demo from its report.
