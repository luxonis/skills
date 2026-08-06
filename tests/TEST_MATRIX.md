# Test matrix

| Case | Entry style | Expected behavior |
| --- | --- | --- |
| Sparse new barcode POC | Natural request | `luxonis-build` discovers context, asks only material questions, and creates a diagrammed plan before code. |
| Detailed new measurement POC | Natural request | Existing detail is reused; the plan addresses depth validity, imaging, load, topology, and countable checks. |
| Plan approval gate | Direct build request with unapproved plan | `awaiting-plan-approval` requires a revisioned plan with no Must-ask decision; no implementation occurs until human approval. |
| Narrow existing-app edit | Natural edit request | The build skill works directly unless the edit changes a material architecture contract. |
| Device-only setup | Direct specialist request | A usable baseline is verified and `DEVICE.md` persists verified facts unless the request is report-only. |
| Pipeline inspection | Direct specialist request | Existing outputs are inspected with bounded commands; an explicitly read-only request never edits source. |
| Broken app | Direct specialist request | The first reproducible failing layer is fixed and rerun before later behavior is changed. |
| External model conversion | Direct specialist request | The skill preserves provenance and distinguishes metadata-valid pending inference from fully archive-ready. |
| Validated model integration | Agent-routed specialist | The archive contract drives preprocessing, parser, output exposure, and representative validation. |
| Training request inside POC | Natural request | Supported OAK work continues while training or dataset construction is isolated into a separate handoff. |
| Generic Python task | Unrelated request | No Luxonis skill should activate. |
| Generic camera buying advice | Unrelated request | No builder workflow should activate without an OAK application-building intent. |

## Objective behavior graders

### New or materially redesigned POC

Pass when the response inspects available project context before questioning, asks a dynamic set
of material questions, draws the proposed data path, names the known-good baseline and the
highest-risk supported assumption, defines observable checks, writes or proposes `POC_PLAN.md`,
and stops for human review. On a sparse prompt, it must pause for Must-ask answers before presenting
a review-ready plan. A fixed three-question interview or a polished plan built around material
`Not yet resolved` contracts is a failure.

### Approved build

Pass when the agent starts from a current matching DepthAI v3 example, proves a direct baseline,
tests the highest-risk supported assumption, builds one customer-specific vertical slice, and
uses direct pipeline plus final-output evidence. A running process alone is not proof.

### Standalone specialist use

Pass when setup, inspect, troubleshoot, convert, and integrate can each complete their narrow job
without a `PROJECT_BRIEF.md` or an artificial return through every other skill. Planning is
optional for narrow specialist work.

### Scope boundary

Pass when unsupported model training, training dataset construction, proprietary SLAM, or a
complete ROS application is isolated behind a concrete interface. The agent must not declare the
overall OAK use case impossible merely because a human-owned subsystem remains.
