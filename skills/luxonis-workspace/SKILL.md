---
name: luxonis-workspace
description: Bootstrap this folder as a Luxonis agent workspace (AGENTS.md, oakctl, udev/host env, project venv/DepthAI v3, CLAUDE.md, docs/glossary.md). Use when AGENTS.md is missing, oakctl is not installed, host udev/env is unready, the project cannot import DepthAI v3, CLAUDE.md needs @AGENTS.md, or docs/glossary.md is missing. Do not use for camera discovery, proving a stream, building an app, product questions, or which camera to buy.
---

# Luxonis Workspace

Make **this folder** a Luxonis agent workspace: host toolchain plus agent files. Not camera
discovery, not proving a stream, not building an app, not product questions.

## Done when

- `oakctl` is on this host, or **blocked** with the current installer command and one next action
- An isolated project env can import DepthAI v3, or **blocked** with one named next action
- `AGENTS.md` exists and is the always-on file
- `CLAUDE.md` includes `@AGENTS.md` and does not duplicate those rules
- `docs/glossary.md` exists (seed if missing)

**Blocked** means one named next action. Ask before sudo.

## 1. Current facts

Use MCP `luxonis__code` for current installer, udev, and CLI facts. Never invent oakctl
subcommands. If MCP is unavailable: https://docs.luxonis.com/software-v3/oak-apps/oakctl.md,
installed `--help`.

## 2. Explore

Read existing `AGENTS.md`, `CLAUDE.md`, `docs/`, the project venv, and `oakctl --version`.
Do not assume a blank repo. Detect and fill what is missing. Never scaffold a second Luxonis
app.

## 3. oakctl

oakctl is required on this computer (udev, inspect, host-run env injection, future host
config).

If missing, get the current installer from MCP or
https://docs.luxonis.com/software-v3/oak-apps/oakctl.md and ask the user to run it. Confirm
the command before quoting it. Current docs (verify): Linux/macOS
`bash -c "$(curl -fsSL https://oakctl-releases.luxonis.com/oakctl-installer.sh)"`; Windows
uses the installer linked from that page.

Host udev/env: take current steps from MCP or installed `--help`. Ask before sudo.

Empty `oakctl list` is not "no device" — that fact lives in `luxonis-device-setup`.

## 4. Isolated Python env

Prefer an existing project venv. DepthAI v3 must import there. Do not global-pip unless
asked. Create a project venv only when none exists.

Confirm with a v3 import in that env, not a guessed version string.

## 5. AGENTS.md

Always-loaded invariants and pointers, not procedures. Seed from
`assets/AGENTS.template.md`.

Prefer `oakctl run-script` when installed `--help` lists it as a local DepthAI environment
runner (`oakctl run-script <command>...`). Confirm on this host; do not invent names. If no
host runner exists, run via the project env and still require oakctl for inspect and udev.
`oakctl hub run-script` (if present) is Hub-token scripts, not a generic host runner.

Do not overwrite a hand-written `AGENTS.md`. Add or update a clearly delimited Luxonis
section.

## 6. CLAUDE.md

If missing, create a file whose body is `@AGENTS.md` (a title only if the host requires one).
If it exists, add `@AGENTS.md` when absent. Never overwrite user content. Do not copy
`AGENTS.md` rules into `CLAUDE.md`.

## 7. Glossary

If `docs/glossary.md` is missing, seed it from `assets/glossary.template.md`. Do not
overwrite a hand-written glossary.

## Do not

- Write `docs/device.md` (`luxonis-device-setup`)
- Scaffold an application (`luxonis-app`)
- Discover cameras or prove a stream (`luxonis-device-setup`)
- Answer which camera to buy (`luxonis`)

## Guardrails

- Ask before sudo, firmware/OS updates, flash, factory reset, Hub adoption, global pip, or
  publishing.
- Never compile DepthAI from source.
- Do not pretend WSL has USB.
- Never run competing processes against one device.
