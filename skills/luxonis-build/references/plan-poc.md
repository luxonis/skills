# Plan a use-case-specific OAK proof of concept

Use this workflow for a new application, plan-only request, or material redesign. Do not write
application code or operate the device while planning.

## Gather before asking

Inspect the request, conversation, repository, device record, available device state,
representative media, current examples, and current model/docs results. Build a private gap list:

- **Known:** stated or directly observed.
- **Inferable:** supported by project, media, device, or current-source evidence.
- **Assumable:** a safe, reversible default can be proposed and tested.
- **Must ask:** the answer could change feasibility, hardware, imaging geometry, perception method,
  model path, runtime topology, external contract, acceptance, or scope.

Before the interview, retrieve only enough current Luxonis context to avoid asking discoverable
questions and to identify which customer facts are material. Defer exhaustive example/model
selection and design-row research until Must-ask answers narrow the architecture.

Ask only material unknowns. There is no question limit. A sparse physical-world request may need a
long interview; a detailed engineering specification may need none.

When the **Must ask** list is nonempty, ask a coherent group of those questions and pause for the
customer's answers. Follow new dependencies in later rounds. Do not choose a convenient runtime,
sensor strategy, external-system contract, or success threshold merely to make the plan look
complete. Assumable and non-blocking unknowns may remain in the plan with explicit validation;
Must-ask unknowns may not be hidden inside `Not yet resolved` fields of a review-ready plan.

A missing fact that can change the architecture is Must-ask. A missing artifact does not block
planning when its contract, acquisition procedure, owner, and later decision gate are already
defined; record it as an implementation or validation dependency instead.

Adapt the interaction:

- For an experienced engineer, ask related questions in efficient groups.
- For an uncertain user, explain why the decision matters, recommend a default, and follow answers
  into dependent questions.
- Prefer "I recommend X because Y; does constraint Z require another choice?" over a blank question
  when current evidence supports a recommendation.
- Do not ask for facts available from source, configuration, device inspection, or media.
- Record non-blocking unknowns as explicit assumptions with validation steps.

Stop interviewing when one credible first-demo architecture and one repeatable success observation
can be specified without an unanswered Must-ask item. Only then write the review-ready plan. Do
not broaden into production requirements.

## Define the first demo

Resolve or explicitly assume:

- Available OAK and intended host-connected or standalone path.
- Real-world decision or action the app enables.
- Exact objects, states, events, text, codes, or measurements.
- Scene geometry, motion, illumination, occlusion, and environmental difficulty that affect the
  chosen method.
- Requested output and any external schema or interaction.
- Representative media path or a concrete capture procedure.
- Observable, countable acceptance checks and the audience judging the demo.
- First-demo boundary and named work deferred to later.

Use `design-review.md` to route only relevant technical decisions. Retrieve current facts instead
of embedding remembered device or API claims in the plan.

## Choose a supported solution path

1. Prefer a supported deterministic method when no learned model is needed.
2. Prefer a compatible Luxonis Model Zoo model returned by MCP.
3. Use a customer-provided model when its contract and license are known.
4. If necessary, shortlist two to four public candidates from original publishers or a reputable
   hub. Include immutable revision, license, input/output/preprocessing, evidence, expected OAK
   path, and gaps. Require approval before download or conversion.
5. Isolate new training or dataset construction as a separate project.

Select one current known-good DepthAI v3 example whose device family, runtime topology, pipeline
shape, model task, and observable outputs best match the first demo. Explain important deltas.

## Balance early success and feasibility

Plan both:

1. **Known-good baseline:** prove the environment, selected device path, capture, and closest
   example work before broad customization.
2. **Highest-risk supported assumption:** make the smallest use-case-specific change that can
   invalidate the selected approach early.

Do not select an unsupported research problem as the autonomous risk test. Define the interface to
human-owned work and continue the useful OAK boundary when possible.

## Draw the pipeline

Include a Mermaid flowchart showing:

- Device, OAK 4 HostNode, external host, and external-system boundaries as applicable.
- Sensors and source streams.
- DepthAI nodes or technically accurate conceptual processing stages.
- Model/deterministic processing and preprocessing/crop stages.
- Tracking, filtering, state, measurement, or decision logic.
- Requested output.
- Inspection topics and evidence points.

Use conceptual labels when an exact node is not yet verified. Do not invent an API name to make the
graph look complete. Keep Mermaid as the canonical portable source even if a richer visual tool is
available.

## Write and review the contract

Create `POC_PLAN.md` from `assets/POC_PLAN.template.md`. Complete every section with a decision,
assumption, or a non-blocking `Not yet resolved`. A Must-ask item blocks a review-ready plan.
Select one first-demo topology rather than simultaneously building host and standalone versions.

Summarize the pipeline and consequential choices. Ask the user to review the interpreted use case,
assumptions, graph, topology, model/method, highest-risk test, inspection contract, and acceptance
checks. Stop **awaiting-plan-approval**. Do not self-approve or continue into implementation.

When the user clearly approves, record the approval text/date and a stable revision without
changing technical content. Any correction invalidates approval and requires another review.
