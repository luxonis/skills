---
name: luxonis
description: Help with Luxonis OAK / DepthAI. Use for questions, choosing a camera, getting hardware working, or routing application work.
---

# Luxonis

Entry skill for Luxonis work in this session. An app in this folder is not required.

## Done when

This request is done. **Blocked** means one named next action. Hardware fault (orange LED,
boot failure, suspected calibration) goes to `support@luxonis.com`.

## 1. Can we work?

- If the MCP tool `luxonis__code` is missing, stop and install the MCP (`https://mcp.luxonis.com/mcp`) in your harness. Verify tool is present after installation or recommend user steps needed for tool to surface.
- If the tool is already available, do not announce a health check.
- Use `luxonis__code` (JavaScript sandbox over models, examples, and docs) for current Luxonis
facts. Never invent DepthAI APIs from memory. DepthAI v3 only; do not mix v2 APIs. Confirm
current node names from MCP or a current example.
- If harness doesn't support MCP, skip MCP installation.
- If tool didn't appear or if MCP is configured but a call fails, rely on `https://docs.luxonis.com/llms.txt` instead.
- Whether using the MCP tool or the live documentation - this will be referred to as <LUXONIS_CONTEXT/> below.

## 2. See what they already asked

Read the request, the repo, `PROJECT_BRIEF.md`, and `DEVICE.md` when they exist. `DEVICE.md`
is setup notes for later sessions - a diary from previous agent: it may list several units and it may be stale. Trust live
state.

If the request already names the job, do that job. If they invoked this skill with nothing to
go on, ask what they need (questions, pick a camera, get hardware working, inspect, record
a scene, fix, convert a model, or build/change an app). Do not start a product interview to
choose the fork.

## 3. Hand off the specialist job

Name the sibling skill and follow it. Do not copy its procedure here.

- Get hardware working for later development → `luxonis-device-setup`
- Build or change an application → `luxonis-app`
- Capture or replay a holistic recording → `luxonis-record`
- The existing app is failing or wrong → `luxonis-troubleshoot`
- They brought a custom model that is not already Zoo-ready → `luxonis-model`

## 4. Questions and advice

Answer from <LUXONIS_CONTEXT/>. Choosing which camera to buy or whether a topology fits lives here, not in
device-setup. Do not write `PROJECT_BRIEF.md` or `POC_PLAN.md` for a question.

## Guardrails

- If you need sudo, ask user for execution by the user.
- Before firmware/OS updates, flash, factory reset, Hub adoption, global pip, or publishing ask user for approval.
- Approval of a named third-party model revision and license authorizes that download. Cloud
  upload stays a separate explicit ask.
- Never compile DepthAI from source.
- Do not pretend WSL has USB.
- Never run competing processes against one device.
