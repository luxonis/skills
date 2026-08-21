# Luxonis Agent Skills

> Experimental direction. This `companion` branch has not been benchmarked with representative
> customer workflows or validated for release. It is not ready for customer use or merge.

Luxonis agent skills for customers using coding agents (Claude Code, Codex, Cursor, Grok) with
OAK cameras and DepthAI.

**`luxonis`** is the entry skill. It checks that MCP is available, then does what you asked:
questions, choosing a camera, getting hardware working, or handing application work to
`luxonis-app`. An application in the folder is not required. A new chat in the same folder
continues from whatever notes and code already exist; it does not restart an interview.

## Advertise this command

Invoke **`luxonis`** for Luxonis work. Compatible hosts may also auto-invoke it from an
ordinary OAK request.

```text
Which OAK should I use for outdoor license-plate reads?
```

```text
Build an OAK application that scans barcodes on packages moving along a conveyor.
```

Claude Code plugin installs may namespace explicit skill commands:

```text
/luxonis-companion:luxonis
```

Codex supports explicit skill selection with:

```text
$luxonis
```

Specialist skills exist and may auto-fire when that is the job. There is no fixed interview
sequence.

| Skill | Job |
| --- | --- |
| `luxonis` | **Primary.** MCP, then questions, device choice, or routing to a specialist. |
| `luxonis-app` | Build or change an application: brief → plan → closed-loop implementation. Hands recording to `luxonis-record`. |
| `luxonis-device-setup` | Get hardware working for later development. Writes setup notes to `DEVICE.md`. |
| `luxonis-record` | Capture or replay a holistic recording of the real scene. |
| `luxonis-inspect` | What a running pipeline is actually producing (`oakctl inspect`). |
| `luxonis-troubleshoot` | An existing app is failing or wrong. |
| `luxonis-model` | Custom (not already Zoo-ready) model → archive → wired in. |

## What survives a new chat

- **`DEVICE.md`** — setup notes for later sessions: host, how cameras show up here, last
  commands that worked. May list several units. Treat as a hint; cabling and IPs change.
- **`PROJECT_BRIEF.md`** — living business problem when you are building or changing an app.
  Not an architecture plan. Not required for questions or setup.
- **`POC_PLAN.md`** — implementation plan, pipeline diagram, UI/output mockup, recording, and
  validation checks for app work.
- **`recordings/`** — holistic source recordings from `luxonis-record`, so later sessions can
  iterate without occupying the camera.
- **The code** — when there is an application.

## Install the full plugin

These draft instructions are pinned to the `companion` branch. Run each command separately and
wait for it to finish before entering the next command.

A full plugin installation includes the seven skills and the Luxonis MCP server at
[https://mcp.luxonis.com/mcp](https://mcp.luxonis.com/mcp). The MCP is bundled through the plugin
configuration. Installing individual skill folders with `npx skills`, a remote rule, or a manual
copy does **not** install the MCP server.

### Claude Code: skills + MCP

First, add the companion marketplace. Enter only this command in Claude Code:

```text
/plugin marketplace add luxonis/skills@companion
```

After Claude confirms that the marketplace was added, install the plugin with a separate command:

```text
/plugin install luxonis-companion@luxonis-companion
```

After installation finishes, reload plugins with a third command:

```text
/reload-plugins
```

If you use the **Add Marketplace** dialog instead of the slash command, enter only
`luxonis/skills@companion` in the marketplace source field. Do not paste the install or reload
commands into that field.

Claude Code may ask you to approve the `luxonis` MCP server the first time it loads. After
approval, verify the connection from a terminal:

```bash
claude mcp list
```

The output should list `luxonis` at `https://mcp.luxonis.com/mcp` as connected.

### Codex: skills + MCP

Codex permits one configured ref for a Git marketplace source. If the V1 `luxonis` marketplace
or the `luxonis-v2-draft` marketplace is already installed, remove that plugin and marketplace
before adding this branch:

```bash
codex plugin remove luxonis@luxonis
codex plugin marketplace remove luxonis
codex plugin remove luxonis-v2-draft@luxonis-v2-draft
codex plugin marketplace remove luxonis-v2-draft
```

First, add the companion marketplace from a terminal:

```bash
codex plugin marketplace add luxonis/skills --ref companion
```

After that command finishes, install the plugin separately:

```bash
codex plugin add luxonis-companion@luxonis-companion
```

Then start a new Codex session so it loads the bundled skills and MCP tools:

```bash
codex
```

You can also open `/plugins` inside Codex, select the `luxonis-companion` marketplace, and
install or enable the plugin there.

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

Use the Claude Code or Codex plugin flow above when testing the complete companion experience.

## Product boundary

The entry skill gets MCP working, then answers Luxonis questions or routes hardware setup and
application work. `luxonis-app` owns product work: a user-provided brief, a plan, and
closed-loop implementation. `luxonis-record` owns capturing and replaying a holistic
recording. Other specialists cover live inspect, a broken existing app, and custom-model
conversion. This plugin does not train a model, construct a training dataset, invent
proprietary SLAM, deliver a complete ROS system, or claim production certification.

Current Luxonis facts come from MCP (`luxonis__code`). Skills add workflow around that:
evidence before live claims, setup notes, a living brief and plan when the job is a product,
and specialist handoff by name.

## Validation

The repository contains deterministic checks for plugin structure, skill files, and local
no-device fixtures:

```bash
python3 tests/validate_static.py
```

These checks do not replace representative agent benchmarks, customer testing, or real-device
validation.

See [the architecture](docs/architecture.md).

## Support

For hardware faults, boot failures, suspected calibration issues, or problems the plugin cannot
resolve locally, contact [support@luxonis.com](mailto:support@luxonis.com) or see the
[Luxonis documentation](https://docs.luxonis.com).

## License

Licensed under the [Apache License 2.0](LICENSE).
