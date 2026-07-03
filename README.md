# Luxonis Agent Skills

Agent skills that help coding agents (Claude Code, Codex, Cursor) work with Luxonis OAK
cameras and DepthAI — from getting a camera working, to shaping a project, to diagnosing
problems.

## Skills

| Skill | What it does |
| --- | --- |
| `luxonis-guide` | Points you to the right skill for your situation. |
| `luxonis-device-setup` | Brings a Luxonis OAK camera to a verified, working state. |
| `luxonis-project-interview` | Interviews you and writes a buildable project brief. |
| `luxonis-build-poc` | Builds a thin runnable proof of concept from a brief. |
| `luxonis-troubleshoot` | Diagnoses broken, slow, or confusing OAK apps and device setups. |

### How they fit together

Most work runs along one path, with troubleshooting available at any point:

1. **Get the camera working** → `luxonis-device-setup`
2. **Turn your idea into a brief** → `luxonis-project-interview`
3. **Build the demo** → `luxonis-build-poc`

Steps 1 and 2 are order-flexible — you can shape the idea before the hardware arrives. If
something breaks along the way, reach for `luxonis-troubleshoot`. Not sure where to start?
Run `luxonis-guide`.

## Install

### Claude Code

```text
/plugin marketplace add luxonis/skills
/plugin install luxonis@luxonis
/reload-plugins
```

### Cursor

Install from the Cursor Marketplace, or add it manually via
**Settings → Rules → Add Rule → Remote Rule (Github)** with:

```text
luxonis/skills
```

### `npx skills`

```bash
npx skills@latest add luxonis/skills
```

## Using the skills

All skills are **manual-only** — you invoke them explicitly, they never trigger on their
own. Invoke by name:

```text
/luxonis-guide
/luxonis-device-setup
/luxonis-project-interview
/luxonis-build-poc
/luxonis-troubleshoot
```

Claude Code plugin installs may namespace skills by plugin name:

```text
/luxonis:luxonis-device-setup
```

## Shared context

Skills that need example code or reference material keep it under a single shared folder so
clones don't get scattered across your machine:

```text
~/.luxonis/agent-context/
```

If a skill populated it earlier, later runs reuse it.

## Support

For hardware faults (orange LED, boot failure, suspected calibration) or issues the skills
can't resolve locally, contact [support@luxonis.com](mailto:support@luxonis.com) or see the
[Luxonis documentation](https://docs.luxonis.com).

## License

Licensed under the [Apache License 2.0](LICENSE).
