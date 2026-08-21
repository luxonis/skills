---
name: luxonis-model
description: Convert or integrate a custom model into an OAK app. Do not use to train a model or to pick a Zoo model for a new app.
---

# Luxonis Model

Take a **custom** (not already Zoo-ready) model to a target NN Archive and wire it into the
OAK app. One skill for convert and integrate.

## Done when

The archive is on disk with a checked contract, and it is wired into the app when that was
requested. Live model behavior is proven when a device or replay (`luxonis-record`) is
available; otherwise name the pending runtime check. **Blocked** means one named next
action.

Read `PROJECT_BRIEF.md`, `DEVICE.md`, source, and any existing archive or conversion note when
present. None is required. Treat `DEVICE.md` as setup notes; trust live state. Do not start a
greenfield interview. If the product is wrong, or the job is picking a Zoo model for a new
app, mention `luxonis-app`.

## 1. Choose the branch

- Source is ONNX, TFLite, OpenVINO IR, or another non-archive artifact → convert
  (`references/convert.md`), then integrate if the app should use it.
- Source is already a target-compatible NN Archive → integrate (`references/integrate.md`).
- Training, dataset collection, or choosing a Zoo model for a new app → say so and stop.

Use MCP `luxonis__code` for current conversion, archive, and integration APIs. Never invent
DepthAI APIs from memory. DepthAI v3 only; do not mix v2 APIs. If MCP is unavailable:
`https://docs.luxonis.com/llms.txt`, installed CLI `--help`, optional cache under
`~/.luxonis/agent-context/`.

## 2. Keep the contract explicit

Before converting or wiring, know:

- Target device and RVC family. RVC2 and RVC4 artifacts are not interchangeable.
- Exact source artifact, checksum, publisher, and accepted license.
- Input names, shapes, layout, dtype, color, and preprocessing.
- Output names, shapes, heads/parser, and label or keypoint order.
- A small representative input set.

Stop rather than guess tensor semantics. Approval of a named third-party model revision and
license authorizes that download. Cloud upload stays a separate explicit ask.

NN Archive metadata is the source of truth for inputs, preprocessing, heads/parser, and
labels. Run `scripts/validate_nn_archive.py` against that contract. Metadata passing is not
proof of useful inference.

## 3. Verify the model path

After convert and/or integrate, compare representative source versus converted behavior when
a supported runtime exists. For live pipeline claims, use `luxonis-inspect`.

If conversion details would help the next session, write a short note next to the archive
(path, target, checksum, parser, labels). That note is not a gate.

## Guardrails

- Ask before cloud upload, global pip, or publishing an archive.
- Keep `HUBAI_API_KEY` and similar credentials in the process environment only.
- Never compile DepthAI from source.
- Never run competing processes against one device.
