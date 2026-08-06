---
name: luxonis-device-setup
description: Identify, connect, and non-destructively verify one Luxonis OAK device and its host-connected or OAK 4 standalone development path. Use for first setup, device discovery, USB or PoE connection, DepthAI or oakctl readiness, a stale DEVICE.md, or when an OAK application cannot yet prove its selected device path. Do not use for a generic application bug after device readiness already passes.
---

# Luxonis Device Setup

Verify one selected OAK far enough to support development. Reachability is not runtime readiness.

End in one state:

- **baseline-ready:** a minimal known-good host or standalone path produces direct camera/app data.
- **device-ready-for-plan:** the device executes the exact path required by `POC_PLAN.md`.
- **blocked:** identify the failing layer, evidence, and one next action.

## Inspect before changing

Read `POC_PLAN.md` and `DEVICE.md` when present. Run
`scripts/luxonis_doctor.py --format json` for non-destructive host facts. Treat recorded device
facts as hints and trust live state.

Use current Luxonis MCP/docs and installed CLI help before forming commands. Distinguish:

- RVC2 devices normally run a DepthAI pipeline on a connected host and need not appear in
  `oakctl`.
- RVC4/OAK 4 devices may run host-connected DepthAI or standalone OAK Apps and may be factory or
  managed through `oakctl`/Hub.
- An empty result from one discovery path does not prove another device family is absent.

If several devices are visible, ask which physical target to use before opening or changing any
device. Pin all subsequent commands to its exact ID, address, or serial.

## Preserve current context

Use `~/.luxonis/agent-context/` as a shared source cache when permitted. Record source URL,
commit/version, and retrieval date. MCP remains the primary live discovery source; a cached
checkout is an exact-source/offline fallback, not permission to use stale APIs silently.

## Verify the selected path

Read `references/readiness-layers.md` and stop at the highest observed layer.

### Host-connected DepthAI

Use an isolated environment. Verify:

1. Supported Python and importable DepthAI v3.
2. The selected device opens from this host with exclusive access.
3. Installed DepthAI version is known and compatible with the selected current example.
4. A minimal known-good pipeline streams one real frame or structured message.
5. The probe closes cleanly and the device remains available.

### Standalone OAK 4 application

Verify:

1. The selected device is RVC4/OAK 4.
2. Current `oakctl` commands and version are known.
3. The device can be selected non-interactively and unambiguously.
4. Authentication and host/device networking required by the app path are available.
5. Managed/factory state, OS, clock, USB composition, or routing do not block the intended path.
6. A minimal known-good OAK App traverses the required build/run path, or an existing app proves
   that path without mutating unrelated state.

Metadata-only device information is not proof that a host pipeline or OAK App runs.

## Troubleshoot one readiness layer

Keep one verification command stable while changing one supported cause:

- Host interpreter, environment, and DepthAI version.
- USB permissions, power, cable, or speed.
- PoE power, routing, DHCP/link-local address, VPN, or firewall.
- Factory versus managed OAK 4 path.
- Exclusive access or stale app/process lock.
- Authentication, clock, network access, or app-build prerequisites.

After a passing project-scoped check, create or update `DEVICE.md` from
`assets/DEVICE.template.md` unless the user requested a report-only/read-only check or there is no
project workspace. Preserve still-valid existing facts and replace stale facts only with live
evidence. Offer compact `AGENTS.md` guidance separately and never overwrite existing instructions.

## Guardrails

- Ask before sudo/admin changes, firmware/OS updates, flashing, factory reset, Hub adoption,
  persistent networking, or deploying over an unrelated running app.
- Never compile DepthAI from source for setup.
- Never pretend a sandbox, VM, or WSL environment has USB or broadcast access it does not have.
- Never run competing probes against one device.
- Stop hardware boot failure, orange LED, electrical fault, or suspected calibration damage at
  `support@luxonis.com`.
