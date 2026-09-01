# Glossary

Short dictionary for this OAK / DepthAI v3 project. Not a tutorial.

- **OAK** — Luxonis spatial AI camera (on-device vision).
- **DepthAI v3** — Current Python API for OAK. Do not mix v2 APIs.
- **RVC2 vs RVC4** — Device compute families. RVC2 runs a DepthAI pipeline on a connected host and does not appear in `oakctl`. RVC4 may be host-connected DepthAI or a standalone OAK App. Artifacts are not interchangeable.
- **oakctl** — Host toolchain: udev, inspect, host-run env injection, OAK Apps, future host config. Empty `oakctl list` is not "no device" (RVC2).
- **Host-connected** — Pipeline runs on this computer against a USB/PoE camera.
- **Standalone OAK App** — Containerized app on the device (`oakapp.toml`, `oakctl app …`).
- **Holistic recording** — Source recording of camera/IMU (and related) for later replay without occupying the camera. Still images and unrelated video are not this.
- **NN Archive** — Packaged model plus metadata for a target RVC family. **Zoo** — published models you pick instead of converting.
- **`docs/brief.md`** — Living business problem. Not a pipeline plan.
- **Dated plans** — `docs/plans/YYYY-MM-DD-<slug>.md` plus `docs/plans/current.md` pointing at the active file. Plans rot; follow `current.md`.
- **`docs/device.md`** — Setup notes, always a hint. Trust live state.
- **Process liveness is not proof** — A running process is not evidence of a correct frame, detection, or output.
