# Test matrix

| Case | Entry style | Expected behavior |
| --- | --- | --- |
| Capability question | Natural request | `luxonis` answers from MCP. No `PROJECT_BRIEF.md`. No device interview. |
| Which OAK to buy | Natural request | `luxonis` advises from MCP. Does not run `luxonis-device-setup`. No brief required. |
| Sparse new barcode app | Natural request | `luxonis` writes `PROJECT_BRIEF.md`, asks only product-changing questions, gets a yes on the use case, then builds from a current DepthAI v3 example. |
| Detailed measurement request | Natural request | Existing detail is reused; few or no questions; no re-interview. |
| Continue with an existing brief | Natural request | The brief is reused; no interview restart; this repo is changed. |
| Narrow existing-app edit | Natural edit request | `luxonis` changes this repo and does not scaffold a new app. |
| Device-only setup | Direct specialist request | Hardware is brought to a usable development path. `DEVICE.md` is setup notes for later sessions (possibly several units), not a singleton lock, unless the request is report-only. |
| Pipeline inspection | Direct specialist request | Existing outputs are inspected with bounded `oakctl inspect`; an explicitly read-only request never edits source. |
| Broken app | Direct specialist request | The first reproducible failing layer is fixed and rerun before later behavior is changed. |
| Custom model | Direct specialist request | `luxonis-model` converts and/or integrates; metadata is not treated as proof of inference. |
| Training / ROS / SLAM request | Natural request | Supported OAK work can continue; training, dataset collection, proprietary SLAM, or a complete ROS system is named and stopped. The OAK use case is not called impossible. |
| Generic Python task | Unrelated request | No Luxonis skill should activate. |
| Generic camera buying advice | Unrelated request | No Luxonis skill should activate for non-OAK camera shopping. |

## Objective behavior graders

### Questions and advice

Pass when `luxonis` uses current Luxonis facts, does not write a brief, and does not force
hardware setup or app scaffolding.

### New app

Pass when the response inspects available project context before questioning, writes or updates
`PROJECT_BRIEF.md` as a product spec (not a pipeline graph), asks only questions that would
change the product, gets a yes on the use case, and starts from a current DepthAI v3 example.
A disposable architecture-plan file or a restarted interview with a matching brief is a failure.

### Existing app

Pass when the agent changes this repo, does not scaffold a new PoC, and uses
`luxonis-inspect` before live-behavior claims.

### Device setup

Pass when a development path streams real data (or a named blocker is reported), `DEVICE.md`
is written as notes that later sessions can read, and the file is not treated as proof that
the desk is unchanged. Several visible units may be recorded. A pin is only for the command
just run.

### Standalone specialist use

Pass when setup, inspect, troubleshoot, and model can each complete their narrow job without a
`PROJECT_BRIEF.md` and without a greenfield interview. If they discover the product is wrong,
they mention `luxonis`.

### Scope boundary

Pass when unsupported model training, training dataset construction, proprietary SLAM, or a
complete ROS application is named and stopped. The agent must not declare the overall OAK use
case impossible merely because a human-owned subsystem remains.
