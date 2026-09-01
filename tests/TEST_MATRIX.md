# Test matrix

| Case | Entry style | Expected behavior |
| --- | --- | --- |
| Capability question | Natural request | `luxonis` answers from MCP. No `docs/brief.md`. No device interview. |
| Which OAK to buy | Natural request | `luxonis` advises from MCP. Does not run `luxonis-device-setup`. No brief required. |
| Workspace setup | Natural request | `luxonis-workspace` installs/asks for oakctl, writes `AGENTS.md`, `@AGENTS.md` in `CLAUDE.md`, seeds `docs/glossary.md` if missing. Does not discover cameras or build an app. |
| Capability first-run | Natural request | `luxonis-app` is not gated on a brief or recording. Copies a current DepthAI v3 example, requires oakctl, proves one real frame or structured message. Live visual claims use `luxonis-inspect`. |
| Sparse new barcode app | Natural request | Product path. `luxonis-app` drafts `docs/brief.md` from stated facts (does not wait on a template), writes `docs/plans/YYYY-MM-DD-<slug>.md` and `docs/plans/current.md` (plan, diagram, UI/output mockup), uses `luxonis-record` when no matching recording exists, then builds from a current DepthAI v3 example and proves it on replay. |
| Detailed measurement request | Natural request | Existing detail is reused; few or no questions; no re-interview. Plan records the stated architecture. Existing recordings are used. |
| Continue with an existing brief | Natural request | The brief is reused; no interview restart; this repo is changed; replay-validated. |
| Narrow existing-app edit | Natural edit request | `luxonis-app` changes this repo and does not scaffold a new app. No new plan unless method, topology, or success checks change. |
| Device-only setup | Direct specialist request | If `AGENTS.md` or oakctl is missing, follow `luxonis-workspace` then continue. Hardware is brought to a usable development path. `docs/device.md` is setup notes for later sessions (possibly several units), not a singleton lock, unless the request is report-only. |
| Pipeline inspection | Direct specialist request | Existing outputs are inspected with bounded `oakctl inspect`; an explicitly read-only request never edits source. |
| Holistic recording | Direct specialist request | `luxonis-record` copies `scripts/holistic_record.py` and captures with that clean recorder (not the product app), preferring `oakctl run-script` when `--help` lists it, then proves the `.tar` with bounded replay. No product interview. |
| Broken app | Direct specialist request | The first reproducible failing layer is fixed and rerun before later behavior is changed. |
| Custom model | Direct specialist request | `luxonis-model` converts and/or integrates; metadata is not treated as proof of inference. |
| Standalone product app | Natural request | `luxonis-app` does not hard-stop when holistic record/replay is unavailable. Proves a named claim with `luxonis-inspect` (or the installed oakctl run path) and states that replay is pending. |
| Training / ROS / SLAM request | Natural request | Supported OAK work can continue; training, dataset collection, proprietary SLAM, or a complete ROS system is named and stopped. The OAK use case is not called impossible. |
| Generic Python task | Unrelated request | No Luxonis skill should activate. |
| Generic camera buying advice | Unrelated request | No Luxonis skill should activate for non-OAK camera shopping. |

## Objective behavior graders

### Questions and advice

Pass when `luxonis` uses current Luxonis facts, does not write a brief or plan, and does not
force hardware setup or app scaffolding.

### Workspace

Pass when `luxonis-workspace` explores the folder first, makes oakctl available (or blocks
with the installer command and one next action), leaves an isolated env that can import
DepthAI v3 (or blocks with one next action), writes or patches `AGENTS.md`, adds `@AGENTS.md`
to `CLAUDE.md` without overwriting user content, and seeds `docs/glossary.md` only if
missing. Fail if it discovers cameras, writes `docs/device.md`, or scaffolds an app.

### Capability first-run

Pass when `luxonis-app` skips brief and recording gates, copies a current DepthAI v3 example,
requires oakctl, and proves one real frame or structured message (live, or replay if a
matching recording exists). Fail if it waits on `docs/brief.md` or refuses to start without a
recording.

### New product app

Pass when `luxonis-app` inspects available project context before questioning, drafts
`docs/brief.md` as a product spec (not a pipeline graph) from stated facts, asks at most
load-bearing missing facts (where output goes; what success looks like), never waits on a
blank template, writes a dated plan at `docs/plans/YYYY-MM-DD-<slug>.md` with
`docs/plans/current.md`, a mermaid diagram, and a UI/output mockup, gets a yes on the use
case and on the plan, names `luxonis-record` when no matching recording exists (and does not
copy that procedure), and starts from a current DepthAI v3 example. A restarted interview
with a matching brief is a failure. Inventing the business problem is a failure. Claiming the
demo works without proof is a failure.

### Existing app

Pass when the agent changes this repo, does not scaffold a new PoC, reuses a matching brief,
and replay-validates via `luxonis-record` (or names the missing recording). Use
`luxonis-inspect` before live-behavior claims.

### Device setup

Pass when a development path streams real data (or a named blocker is reported),
`docs/device.md` is written as notes that later sessions can read, and the file is not
treated as proof that the desk is unchanged. Several visible units may be recorded. A pin is
only for the command just run. oakctl is required; if it is missing, `luxonis-workspace`
runs first.

### Standalone specialist use

Pass when setup, record, inspect, troubleshoot, and model can each complete their narrow job
without a `docs/brief.md` and without a greenfield interview. If they discover the product
is wrong, they mention `luxonis-app`. If `AGENTS.md` or needed oakctl is missing, they name
`luxonis-workspace` then continue.

Pass when a standalone OAK App (or topology that cannot holistic-record) can still complete
`luxonis-app` via `luxonis-inspect` or the current oakctl run path, with replay marked
pending.

### Scope boundary

Pass when unsupported model training, training dataset construction, proprietary SLAM, or a
complete ROS application is named and stopped. The agent must not declare the overall OAK use
case impossible merely because a human-owned subsystem remains.
