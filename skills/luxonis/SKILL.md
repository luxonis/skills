---
name: luxonis
description: Help with Luxonis OAK / DepthAI questions, which camera to buy, or any OAK request that is not already a workspace, device-setup, build, record, inspect, fix, or convert job.
---

# Luxonis

Entry skill for Luxonis work in this session. An app in this folder is not required.

## Done when

This request is done. **Blocked** means one named next action. Hardware fault (orange LED,
boot failure, suspected calibration) goes to `support@luxonis.com`.

## 1. Can we work?

Current Luxonis facts come from the Luxonis MCP server (`luxonis`,
`https://mcp.luxonis.com/mcp`). The surfaced tool names vary by host. In order:

1. If those tools are available, use them. Do not announce a health check.
2. If they are missing and this host supports MCP, tell the user how to enable the server here
   and stop until it surfaces. The full plugin install bundles the server; otherwise add
   `https://mcp.luxonis.com/mcp` in the host's MCP settings.
3. If this host cannot use MCP, or configured calls fail, use
   `https://docs.luxonis.com/llms.txt` and say facts come from the docs fallback.

Never invent DepthAI APIs from memory. DepthAI v3 only; do not mix v2 APIs. Confirm current
node names from MCP or a current example.

Best source first: the Luxonis MCP tools (surfaced names vary by host), then the exact example
or doc source they return, then `https://docs.luxonis.com/llms.txt`, then observed behavior;
memory is only for general reasoning. For oakctl commands and flags, the installed
`oakctl --help` outranks docs and MCP: the local version (possibly older or beta) defines what
is possible here, so work from it and suggest an oakctl update when it lacks something current
docs describe. If observed host or device behavior contradicts docs or MCP, trust the
observation and note the conflict. If offline, work from `oakctl --help` and local examples and
name which facts are unverified.

The source in use, MCP tools or live documentation, is referred to as <LUXONIS_CONTEXT/>
below.

## 2. Workspace

If `AGENTS.md` is missing, or oakctl is missing when this job needs the host toolchain, name
`luxonis-workspace` and follow it, then continue. Do not copy its procedure.

## 3. See what they already asked

Read the request, the repo, `docs/brief.md`, and `docs/device.md` when they exist. Also read
legacy root `PROJECT_BRIEF.md` and `DEVICE.md` if present; write new work to the `docs/`
paths. `docs/device.md` is setup notes for later sessions — a diary from a previous agent: it
may list several units and it may be stale. Trust live state.

If the request already names the job, do that job. If they invoked this skill with nothing to
go on, ask what they need (questions, pick a camera, host toolchain / AGENTS.md, get hardware
working, record a scene, fix, convert a model, or build/change an app). Do not start a product
interview to choose the fork.

## 4. Hand off the specialist job

Name the sibling skill and follow it. Do not copy its procedure here.

- Host toolchain / AGENTS.md / oakctl install → `luxonis-workspace`
- Hardware working / camera not found → `luxonis-device-setup`
- Build or change an application → `luxonis-app`
- Holistic recording → `luxonis-record`
- Live inspect of a running pipeline → `luxonis-inspect`
- Existing app failing → `luxonis-troubleshoot`
- Custom not-Zoo-ready model → `luxonis-model`

## 5. Questions and advice

Answer from <LUXONIS_CONTEXT/>. Choosing which camera to buy or whether a topology fits lives
here, not in device-setup. Do not write `docs/brief.md` or a plan for a question.

## Guardrails

- If you need sudo, ask user for execution by the user.
- Before firmware/OS updates, flash, factory reset, Hub adoption, global pip, or publishing ask user for approval.
- Approval of a named third-party model revision and license authorizes that download. Cloud
  upload stays a separate explicit ask.
- Never compile DepthAI from source.
- Do not pretend WSL has USB.
- Never run competing processes against one device.
