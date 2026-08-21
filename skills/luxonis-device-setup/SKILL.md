---
name: luxonis-device-setup
description: Get Luxonis OAK hardware working for development and write setup notes. Use for first setup, USB/PoE, oakctl or DepthAI discovery, or a camera that is not found.
---

# Luxonis Device Setup

Get OAK hardware working so later development can use it. This can happen before any app
exists. Do not start a product interview. Questions or camera advice → `luxonis`. Build or
change an app → `luxonis-app`. oakctl install and `AGENTS.md` → `luxonis-workspace`.

## Done when

A host-connected or standalone path streams real camera or app data, and `docs/device.md`
holds setup notes for the next session (unless the user asked for a report-only check).
Notes may describe several units. **Blocked** means the failing layer, the evidence, and one
next action. Hardware fault (orange LED, boot failure, suspected calibration) goes to
`support@luxonis.com`.

## 1. Current facts

Use MCP `luxonis__code` and installed CLI help before forming commands. Never invent DepthAI
APIs from memory. DepthAI v3 only. If MCP is unavailable: `https://docs.luxonis.com/llms.txt`,
installed `--help`.

oakctl is required on this host (udev, inspect, future host config). If `AGENTS.md` is
missing, or oakctl is missing, name `luxonis-workspace` and follow it, then continue hardware
proof. Do not copy its procedure.

## 2. Inspect before changing

Read `docs/device.md` when present as notes, not ground truth. Also read a legacy root
`DEVICE.md` if present; write new notes to `docs/device.md`. Cabling, IPs, and which unit is
on the desk can change. Run `scripts/luxonis_doctor.py --format json` for non-destructive
host facts. Trust live state over the file.

- RVC2 runs a DepthAI pipeline on a connected host and does not appear in `oakctl`. Empty
  `oakctl list` does not mean no device.
- RVC4 may be host-connected DepthAI or a standalone OAK App.
- Prefer DepthAI discovery for first contact; it sees both families.

Discover what is attached. Several units is normal; record them. Pin an id, address, or serial
only for **this command** (open, flash, adopt, `oakctl -d`). Do not treat that pin as the only
legal device for this folder.

Ask which physical camera only when a privileged or mutating action would be ambiguous.
Serialize probes; never run competing processes against one device.

## 3. Get a development path working

Stop at the highest layer proven by direct observation: discovered, reachable, or ready
(real frame or message). Device metadata is not proof that a pipeline or OAK App runs. Prove
the path the user cares about; if they did not specify, prove what is present. Two cameras
means two notes, not a forced winner.

### Host-connected DepthAI

Use an isolated environment:

1. Supported Python and importable DepthAI v3.
2. The device for this check opens from this host with exclusive access.
3. A minimal known-good pipeline streams one real frame or structured message.
4. The probe closes cleanly and the device remains available.

### Standalone OAK 4

1. The device for this check is RVC4.
2. Current `oakctl` commands and version are known.
3. The device can be selected non-interactively for this command.
4. Authentication and host/device networking required by the path are available.
5. A minimal known-good OAK App traverses the required build/run path, or an existing app
   proves that path without mutating unrelated state.

## 4. Troubleshoot one readiness layer

Keep one verification command stable while changing one supported cause: interpreter and
DepthAI version; USB permissions, power, cable, or speed; PoE power, routing, DHCP/link-local,
VPN, or firewall; factory versus managed OAK 4; exclusive access; authentication or clock.

Confirm current USB, PoE, and discovery details from docs. Useful starting hints: Linux USB
RVC2 may appear as Movidius `03e7:2485`; a red LED on OAK 4 often means insufficient PoE
power.

## 5. Write setup notes

Create or update `docs/device.md` from `assets/DEVICE.template.md` unless the user requested
a report-only check or there is no project workspace. Include host facts, each unit seen,
last proving command per path, and open issues. Preserve still-valid notes; replace stale
facts with live evidence. A blocked session should still leave notes about what failed.

## Guardrails

- Ask before sudo/admin changes, firmware/OS updates, flashing, factory reset, Hub adoption,
  global pip, persistent networking, or deploying over an unrelated running app.
- Never compile DepthAI from source.
- Do not pretend a sandbox, VM, or WSL environment has USB or broadcast access it does not
  have.
- Never run competing probes against one device.
