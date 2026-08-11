# Luxonis Agent Skills: V2 Draft

> Experimental direction only. This branch has not been benchmarked with representative customer
> workflows or validated for release. It is not ready for customer use or merge.

This draft explores the next step for Luxonis agent support: moving from example-level OAK
onboarding to a working, use-case-specific proof of concept that an engineer can evaluate and
extend.

## What the plugin includes

A full plugin installation includes:

- Six OAK and DepthAI skills for planning, building, setup, inspection, troubleshooting, and model
  workflows.
- The Luxonis MCP server at [https://mcp.luxonis.com/mcp](https://mcp.luxonis.com/mcp), which
  supplies current documentation, examples, platform context, and model information.

The MCP is bundled through the plugin configuration. Installing individual skill folders with
`npx skills`, a remote rule, or a manual copy does **not** install the MCP server.

## Install the full plugin

These draft instructions are pinned to the `v2-draft` branch. Run each command separately and wait
for it to finish before entering the next command.

### Claude Code: skills + MCP

First, add the draft marketplace. Enter only this command in Claude Code:

```text
/plugin marketplace add luxonis/skills@v2-draft
```

After Claude confirms that the marketplace was added, install the plugin with a separate command:

```text
/plugin install luxonis-v2-draft@luxonis-v2-draft
```

After installation finishes, reload plugins with a third command:

```text
/reload-plugins
```

If you use the **Add Marketplace** dialog instead of the slash command, enter only
`luxonis/skills@v2-draft` in the marketplace source field. Do not paste the install or reload
commands into that field.

Claude Code may ask you to approve the `luxonis` MCP server the first time it loads. After
approval, verify the connection from a terminal:

```bash
claude mcp list
```

The output should list `luxonis` at `https://mcp.luxonis.com/mcp` as connected.

### Codex: skills + MCP

Codex permits one configured ref for a Git marketplace source. If the V1 `luxonis` marketplace is
already installed, remove that plugin and marketplace before adding the draft:

```bash
codex plugin remove luxonis@luxonis
codex plugin marketplace remove luxonis
```

First, add the draft marketplace from a terminal:

```bash
codex plugin marketplace add luxonis/skills --ref v2-draft
```

After that command finishes, install the plugin separately:

```bash
codex plugin add luxonis-v2-draft@luxonis-v2-draft
```

Then start a new Codex session so it loads the bundled skills and MCP tools:

```bash
codex
```

You can also open `/plugins` inside Codex, select the `luxonis-v2-draft` marketplace, and install
or enable the plugin there.

### Skills-only alternatives

These options expose the skill instructions but do not install the bundled MCP server.

For Cursor, install from the Cursor Marketplace or add a remote rule from:

```text
luxonis/skills
```

With `npx skills`:

```bash
npx skills@latest add luxonis/skills
```

Use the Claude Code or Codex plugin flow above when testing the complete V2 experience.

## Proposed skills

| Skill | Purpose |
| --- | --- |
| `luxonis-build` | Plan, build, inspect, and iterate on an OAK proof of concept. |
| `luxonis-device-setup` | Verify one OAK device and its development path. |
| `luxonis-inspect-pipeline` | Capture and interpret bounded live pipeline evidence. |
| `luxonis-troubleshoot` | Diagnose the first reproducible failing OAK layer. |
| `luxonis-convert-model` | Convert and validate an approved model for a named RVC target. |
| `luxonis-integrate-model` | Integrate a validated Zoo model or NN Archive into an OAK app. |

Compatible hosts may select these skills from an ordinary OAK request. Customers should not need
to study the skill list or manually execute a fixed sequence. They can also invoke a skill
explicitly when they want a narrow workflow.

For example:

```text
Build an OAK application that scans barcodes on packages moving along a conveyor.
```

Claude Code plugin installs may namespace explicit skill commands:

```text
/luxonis-v2-draft:luxonis-build
```

Codex supports explicit skill selection with:

```text
$luxonis-build
```

## V2 workflow

For a new or materially redesigned proof of concept, `luxonis-build` gathers only the missing
material constraints, draws the proposed pipeline, and asks for human review before implementation.
After approval, it builds a thin vertical slice and iterates from direct pipeline and final-output
evidence.

The specialist skills remain independently useful and may be selected by the agent for device
readiness, pipeline inspection, troubleshooting, model conversion, or model integration.

## Product boundary

V2 owns an OAK/DepthAI proof-of-concept vertical slice, supported model conversion and integration,
inspection, and observable application behavior. It does not autonomously train a model, construct
a training dataset, invent proprietary SLAM, deliver a complete ROS system, or claim production
readiness.

The model and coding harness perform most of the engineering work. The MCP provides current
Luxonis facts, while the skills add focused workflow, review, evidence, and scope controls.

## Draft validation

The repository contains deterministic checks for plugin structure, skill contracts, and local
no-device fixtures:

```bash
python3 tests/validate_static.py
```

These checks do not replace representative agent benchmarks, customer testing, or real-device
validation.

See [the architecture](docs/architecture.md) and [the short RFC](docs/v2-draft-rfc.md).

## Support

For hardware faults, boot failures, suspected calibration issues, or problems the plugin cannot
resolve locally, contact [support@luxonis.com](mailto:support@luxonis.com) or see the
[Luxonis documentation](https://docs.luxonis.com).

## License

Licensed under the [Apache License 2.0](LICENSE).
