---
name: luxonis-guide
description: "Choose the right Luxonis skill for your current situation."
disable-model-invocation: true
argument-hint: "what are you trying to do?"
allowed-tools: Bash(ls *) Bash(cat *) Bash(grep *) Bash(echo *) Bash(head *) Bash(true)
metadata:
  author: luxonis
  version: "1.0.0"
  status: stable
---

# Luxonis Guide

Route the user to **one** Luxonis skill that fits their current situation. Recommend the
next command and stop. Do not do that skill's work here.

End in exactly one state:

- **routed** -- name one next command and where it sits on the flow.
- **out-of-scope** -- the situation is not served by the phase-one skills; name the gap and
  point to docs or support.

## The flow

Most work runs along one spine, with one side path.

**Main flow: idea -> working demo**

1. **Get the camera working** -> `luxonis-device-setup`
2. **Turn the idea into a brief** -> `luxonis-project-interview`
3. **Build the thin PoC** -> `luxonis-build-poc`

Steps 1 and 2 are **order-flexible**: the interview works with no device yet, so a user
waiting on hardware can sharpen the idea first. Step 3 is the convergence point -- it wants
both a brief and a verified device.

**Side path: something is broken, slow, or confusing** -> `luxonis-troubleshoot`. Branch off
at any point, then come back to the spine.

## 1. Read the situation

Preflight the current working directory for flow markers. Existence is the signal; do not
deep-parse.

!`ls -1 2>/dev/null | grep -E '^(DEVICE|PROJECT_BRIEF)\.md$' || echo "no markers"`

!`cat PROJECT_BRIEF.md 2>/dev/null | head -3 || true`

On agents that support shell injection (e.g. Claude Code) the lines above are filled in
before routing. On agents that do not, ignore them and list the directory / read
`PROJECT_BRIEF.md` yourself.

Combine the markers with what the user said:

- `DEVICE.md` present -> a device was already verified here.
- `PROJECT_BRIEF.md` present -> the idea was already shaped into a brief.

## 2. Route

Map the situation to one entry:

- New camera, or unsure it works / connects -> **`luxonis-device-setup`**.
- Has a working camera (or `DEVICE.md`) but no `PROJECT_BRIEF.md`, and wants to build
  something -> **`luxonis-project-interview`**.
- `PROJECT_BRIEF.md` exists and the user wants it running -> **`luxonis-build-poc`**.
- An app, pipeline, or device **discovery** is broken, slow, or confusing ->
  **`luxonis-troubleshoot`**.

If the situation is clear, route immediately. If it is ambiguous (no argument, or something
vague like "help with my OAK"), ask **exactly one** clarifying question, then commit:

> Do you already have a camera connected and working, or are you starting from just an idea?

Never ask a second question. Never start shaping the idea -- that is
`luxonis-project-interview`'s job, not this router's.

### Broken device vs broken software

"My camera isn't working" splits two ways. This is the spot where the one clarifying
question earns its keep:

- Broken **software** -- discovery fails, pipeline errors, bad depth, low FPS, unclear
  output -> `luxonis-troubleshoot`.
- Broken **device** -- orange LED, won't boot, suspected calibration fault -> this is a
  hardware fault. Go **out-of-scope** to `support@luxonis.com`, not troubleshoot.

## 3. End

**routed** -- name the next command and one line on where it sits:

> Run `/luxonis-device-setup` next -- that verifies the camera, then we shape the idea and
> build.

Plugin installs may namespace the command, e.g. `/luxonis:luxonis-device-setup`.

**out-of-scope** -- do not force a route. Name the gap and point onward:

- Hardware fault (orange LED, boot failure, calibration) -> `support@luxonis.com`.
- V2 -> V3 migration -> no skill yet; point to the docs below (a skill may come later).
- Anything else outside the four skills (non-OAK hardware, production/fleet deployment at
  scale) -> name it and point to https://docs.luxonis.com.

## Docs

- Software hub / getting started -- https://docs.luxonis.com/software-v3.md
- Troubleshooting index -- https://docs.luxonis.com/software-v3/troubleshooting.md
