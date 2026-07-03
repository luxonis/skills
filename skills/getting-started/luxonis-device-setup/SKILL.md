---
name: luxonis-device-setup
description: "Bring a Luxonis OAK camera to a verified device-ready state."
disable-model-invocation: true
argument-hint: "device model, OS, and connection topology"
metadata:
  author: luxonis
  version: "1.0.0"
  status: stable
---

# Luxonis Device Setup

Reach **device-ready**: one target OAK is identified and one minimal, rerunnable check
proves it is usable from this host. Stop there; route app-building to
`luxonis-project-interview`.

End in exactly one state:

- **device-ready** -- report model/family, connection, device id/IP/serial, and the exact
  verification command or snippet.
- **blocked** -- report one blocking layer, evidence, and the next action.

## 1. Probe before asking

First run a **discovery pass**, not a verification pass:

- Check host facts: OS, Python, `depthai` import, USB, network/VPN clues, and existing
  `oakctl`.
- If `depthai` is missing, install it in an isolated venv with a supported Python. Do not
  use global `pip` or edit project deps without approval.
- Run DepthAI discovery. Use `oakctl` discovery only if `oakctl` is already installed.
- If discovery can open a device, read its calibration product name and close it.

Family rules:

- **OAK / RVC2** -- DepthAI only. It never appears in `oakctl`. USB models may first appear
  as `03e7:2485` Movidius/MyriadX; PoE RVC2 is still DepthAI.
- **OAK4 / RVC4** -- factory-state devices can be verified with DepthAI. `oakctl` is for the
  managed control plane: Hub adoption, standalone app/device management, updates, USB
  internet sharing. Once adopted/configured into managed mode, manage it via Hub or `oakctl`.

Prefer DepthAI discovery for first contact: it sees both families. `oakctl list` only shows
RVC4 and only matters when `oakctl` is already installed or management is required; an empty
`oakctl list` is not evidence that an RVC2 OAK is missing.

### Target gate

After the discovery pass, build a short list of visible candidates. If there is more than
one candidate and the user's target is not explicit, **stop and ask one target question**
before any verification:

> I can see A and B. Which physical OAK should I verify?

Do not run `oakctl connect`, `oakctl device info`, oak-agent `curl` probes, frame streaming,
udev changes, updates, adoption, or flashing until the target is identified. Unknown target
is an interview checkpoint, not a blocked state.

After the target is identified, pin later commands to that device id/IP/serial.

## 2. Verify once

Use the smallest rerunnable check that matches the device state:

- **Factory OAK4 / RVC4** -- a throwaway DepthAI device-info/frame check is enough for
  baseline readiness. Do not install `oakctl` just because the model is OAK4.
- **OAK / RVC2** -- use DepthAI; confirm the device opens and streams a frame. On Linux USB,
  add the Movidius udev rule only if permissions block access.
- **Managed OAK4 / RVC4** -- use Hub or `oakctl` only after the target gate selects that
  managed device. If `oakctl` is required and absent, ask the user to install it themselves:
  Linux/macOS installer:
  `bash -c "$(curl -fsSL https://oakctl-releases.luxonis.com/oakctl-installer.sh)"`
  Windows MSI:
  `https://oakctl-releases.luxonis.com/data/latest/windows_x86_64/oakctl.msi`
  After the user confirms it is installed, verify with `oakctl device list --format json`
  plus `oakctl device info -d <ip-or-serial> --format json` or the current
  `oakctl device ...` equivalent. If a password prompt appears, stop and ask for the
  password or ask the user to run the interactive command; do not probe oak-agent endpoints
  manually.

## 3. Troubleshoot one layer at a time

Change one thing, rerun the same verification, observe.

- **PoE/Ethernet** -- red LED on OAK4: insufficient power, require PoE+ 802.3at / 30W. No
  DHCP: use link-local `169.254.0.0/16` or fix DHCP. Discovery blocked: disable VPN, check
  routing, allow `11491/udp` and `11490/tcp` for OAK4.
- **USB** -- no devices or USB2 fallback: use a USB3 port and known-good USB3 cable (<2 m).
  Brownout: external power/powered hub. Linux permission error: add the udev rule. RVC2
  flaky USB3: try forcing USB2 (`maxUsbSpeed=dai.UsbSpeed.HIGH`).
- **Tool mismatch** -- RVC2 in `oakctl` is expected to fail; switch to DepthAI. OAK4
  management issues belong to Hub/`oakctl`; update tools only when needed and with approval.

## 4. Persist handoff context

After **device-ready**, actively offer to save the setup for later agent sessions. Use a
clear permission flow; do not end by merely saying `AGENTS.md`/`CLAUDE.md` were not
modified.

1. Ask whether to create/update project-root `DEVICE.md`. If the user declines persistence,
   stop. If yes, save only this project's verified device facts: date, model/product name,
   family, connection/topology, id/IP/serial, managed state (`factory` vs
   `Hub/oakctl-managed`), required tooling, and the exact verification command/snippet.
2. After `DEVICE.md` is saved, before ending, unless the user already approved or declined
   it, ask a separate explicit guidance-file question, for example:

   > Saved `DEVICE.md`. Should I also create/update `AGENTS.md` or `CLAUDE.md` with the
   > compact Luxonis handoff block? If neither exists, I can create `AGENTS.md`.

3. Create/update `AGENTS.md` or `CLAUDE.md` only after that approval; patch existing files.
   Add or update a compact block:

   ```xml
   <luxonis-context>
   Read project if exists `DEVICE.md` before OAK work and pin commands to that device.
   Use https://docs.luxonis.com/llms.txt as the Luxonis docs source map.
   Check `~/.luxonis/agent-context/` if present; it is shared Luxonis context for cloned
   repos, docs, examples, and reusable notes, not this project's device record.
   Update `DEVICE.md` whenever adoption, IP, cabling, or management state changes.
   </luxonis-context>
   ```

## Guardrails

- Run non-privileged discovery yourself. Installing `depthai` into an isolated runner is
  part of discovery; request approval for sudo/admin changes or project dependency changes.
- Do not pretend WSL has USB access. If the agent runs in WSL and the target is USB, stop
  until the user exposes the device to WSL, e.g. with `usbipd`, or runs the workflow from a
  host with direct USB access.
- Do not require GUI tools. Accept OAK Viewer evidence if the user already has it, but do
  not install or drive it as the agent path.
- Confirm device updates, flashing, factory reset, and Hub adoption before doing them.
- Never compile DepthAI from source; if that seems required, mark **blocked**.
- Orange LED, boot failure, or suspected calibration fault -> **blocked** and contact
  support@luxonis.com.

## Docs

- OAK4 getting started -- https://docs.luxonis.com/hardware/platform/deploy/oak4-deployment-guide/oak4-getting-started.md
- OAK USB getting started -- https://docs.luxonis.com/hardware/platform/deploy/usb-deployment-guide.md
- DepthAI Device Information -- https://docs.luxonis.com/software-v3/depthai/examples/misc/device_information.md
- `oakctl` CLI -- https://docs.luxonis.com/software-v3/oak-apps/oakctl.md
