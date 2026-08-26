# Luxonis Agent Skills

> Beta. Skill behavior and project file layout may still change between releases. Feedback
> and issues: [support@luxonis.com](mailto:support@luxonis.com).

Luxonis agent skills for customers using coding agents (Claude Code, Codex, Cursor, Grok) with
OAK cameras and DepthAI.

**`luxonis`** is the entry skill. It checks that MCP is available, gates on workspace when
`AGENTS.md` or oakctl is missing, then does what you asked: questions, choosing a camera, or
handing a named job to a specialist. An application in the folder is not required. A new chat
in the same folder continues from whatever notes and code already exist; it does not restart
an interview.

oakctl is the host toolchain (udev, inspect, host-run env injection, future host config).

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
/luxonis:luxonis
```

Codex supports explicit skill selection with:

```text
$luxonis
```

Specialist skills exist and may auto-fire when that is the job. There is no fixed interview
sequence. Ceremony follows the request: a named capability (show depth, stream RGB) is a
first-run, not a product brief.

| Skill | Job |
| --- | --- |
| `luxonis` | **Primary.** MCP, workspace gate, then questions, device choice, or routing to a specialist. |
| `luxonis-workspace` | Make this folder a Luxonis agent workspace: oakctl, AGENTS.md, project env, glossary. |
| `luxonis-app` | Build or change an application. Capability first-run, or product `docs/brief.md` plus a dated plan. Hands recording to `luxonis-record`. |
| `luxonis-device-setup` | Get hardware working for later development. Writes setup notes to `docs/device.md`. |
| `luxonis-record` | Capture or replay a holistic recording of the real scene. |
| `luxonis-inspect` | What a running pipeline is actually producing (`oakctl inspect`). Proof tool; not on the entry job list. |
| `luxonis-troubleshoot` | An existing app is failing or wrong. |
| `luxonis-model` | Custom (not already Zoo-ready) model → archive → wired in. |

## What survives a new chat

Customer project files (the user's repo). This repository's `docs/architecture.md` is not
that layout.

Living (overwrite in place):

- **`AGENTS.md`** — always-on invariants and pointers. `CLAUDE.md` includes `@AGENTS.md`.
- **`docs/glossary.md`** — vocabulary for this project.
- **`docs/brief.md`** — living business problem when you are building a product app. Not an
  architecture plan. Not required for questions, setup, or a capability first-run.
- **`docs/device.md`** — setup notes for later sessions: host, how cameras show up here, last
  commands that worked. May list several units. Treat as a hint; cabling and IPs change.
- **The code** — when there is an application.

Dated (plans rot):

- **`docs/plans/YYYY-MM-DD-<slug>.md`** — implementation plan, pipeline diagram, UI/output
  mockup, recording, and validation checks for product app work.
- **`docs/plans/current.md`** — stub that points at the current plan file.

Stay out of `docs/`: **`recordings/`** (holistic source recordings from `luxonis-record`) and
**`evidence/`** (inspect/replay working files).

If a folder still has root `PROJECT_BRIEF.md`, `POC_PLAN.md`, or `DEVICE.md`, skills read
those and write the new paths.

## Install the full plugin

Run each command separately and wait for it to finish before entering the next command.

A full plugin installation includes the eight skills and the Luxonis MCP server at
[https://mcp.luxonis.com/mcp](https://mcp.luxonis.com/mcp). The MCP is bundled through the plugin
configuration. Installing individual skill folders with `npx skills`, a remote rule, or a manual
copy does **not** install the MCP server.

This repository ships the standardized [Agent Plugins](https://agent-plugins.org/) layout
(root `plugin.json`, `mcp.json`, and `skills/`), which Codex and Cursor load directly.
`.claude-plugin/` plus `.mcp.json` remain for Claude Code. Use a recent Codex release; older
releases only read the legacy `.codex-plugin/` manifest, which this repository no longer
provides.

### Claude Code: skills + MCP

First, add the marketplace. Enter only this command in Claude Code:

```text
/plugin marketplace add luxonis/skills
```

After Claude confirms that the marketplace was added, install the plugin with a separate command:

```text
/plugin install luxonis@luxonis
```

After installation finishes, reload plugins with a third command:

```text
/reload-plugins
```

If you use the **Add Marketplace** dialog instead of the slash command, enter only
`luxonis/skills` in the marketplace source field. Do not paste the install or reload
commands into that field.

Claude Code may ask you to approve the `luxonis` MCP server the first time it loads. After
approval, verify the connection from a terminal:

```bash
claude mcp list
```

The output should list `luxonis` at `https://mcp.luxonis.com/mcp` as connected.

### Codex: skills + MCP

Add the marketplace from a terminal:

```bash
codex plugin marketplace add luxonis/skills
```

After that command finishes, install the plugin separately:

```bash
codex plugin add luxonis@luxonis
```

Then start a new Codex session so it loads the bundled skills and MCP tools:

```bash
codex
```

You can also open `/plugins` inside Codex, select the `luxonis` marketplace, and
install or enable the plugin there.

### Cursor: skills + MCP

Cursor loads the standardized Agent Plugins layout without changes. The plugin is not yet
listed on the Cursor Marketplace. Until it is, clone this repository into
`~/.cursor/plugins/local/luxonis` (or symlink it there) and restart Cursor. On Cursor Teams
or Enterprise, an admin can instead add this repository as a team marketplace (Dashboard →
Plugins → Add Marketplace → Import from Repo) so members install it with one click. Plugin
installs include the bundled MCP server from `mcp.json`.

### Skills-only alternatives

These options expose the skill instructions but do not install the bundled MCP server.

For Cursor, a remote rule (without the plugin) stays skills-only:

```text
luxonis/skills
```

With `npx skills`:

```bash
npx skills@latest add luxonis/skills
```

Use a plugin flow above for the complete experience.

## What this plugin does not do

This plugin does not train a model, construct a training dataset, invent proprietary SLAM,
deliver a complete ROS system, or claim production certification. When a request needs one of
those, the skills name it and stop, without calling the OAK use case impossible.

Current Luxonis facts come from the Luxonis MCP server's `code` tool. Skills add workflow
around that: evidence before live claims, setup notes, a living brief and dated plan when
the job is a product, and specialist handoff by name.

## Developing

Developer documentation lives under [`docs/`](docs/): [architecture](docs/architecture.md)
and [testing](docs/testing.md).

## Support

For hardware faults, boot failures, suspected calibration issues, or problems the plugin cannot
resolve locally, contact [support@luxonis.com](mailto:support@luxonis.com) or see the
[Luxonis documentation](https://docs.luxonis.com).

## License

Licensed under the [Apache License 2.0](LICENSE).
