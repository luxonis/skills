# Agent notes (Luxonis)

This is a Luxonis OAK / DepthAI v3 project.

## Facts

- Current APIs, examples, and models come from the `code` tool on the Luxonis MCP server (`luxonis`, `https://mcp.luxonis.com/mcp`); the surfaced tool name varies by host. Never invent DepthAI APIs from memory.
- DepthAI v3 only. Do not mix v2 APIs.
- Confirm node names from MCP and oakctl flags from `oakctl --help`. The installed oakctl
  version defines what is possible here; suggest an oakctl update when it lacks something
  current docs describe.
- If observed host or device behavior contradicts docs or MCP, trust the observation and note the conflict.
- If offline, work from `oakctl --help` and local examples and name which facts are unverified.

## How this repo runs

- `oakctl` is the host toolchain (udev, inspect, host-run env, future host config).
- Prefer `oakctl run-script` for host runs when `oakctl --help` lists it as a local DepthAI environment runner; do not invent subcommands. If no host runner exists, run via this project's isolated env and still use oakctl for inspect and udev.
- `oakctl hub run-script` (if present) is Hub-token scripts, not a generic host runner.
- Replay: `DEPTHAI_REPLAY` / current holistic replay from docs. Do not occupy the camera when a matching recording exists.
- Never run competing processes against one device.

## Pointers

- Vocabulary: `docs/glossary.md`
- Business problem: `docs/brief.md`
- Hardware notes (hint; trust live state): `docs/device.md`
- Current implementation plan: `docs/plans/current.md`
- Jobs: `luxonis` (questions / which camera), `luxonis-workspace` (this folder's toolchain and agent files), `luxonis-device-setup` (hardware working), `luxonis-app` (build or change an app), `luxonis-record` (holistic recording), `luxonis-inspect` (live pipeline evidence), `luxonis-troubleshoot` (existing app failing), `luxonis-model` (custom not-Zoo-ready model)
