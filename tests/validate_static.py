#!/usr/bin/env python3
"""Deterministic structure and no-device checks for V2 Lightweight."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "luxonis-build",
    "luxonis-device-setup",
    "luxonis-inspect-pipeline",
    "luxonis-troubleshoot",
    "luxonis-convert-model",
    "luxonis-integrate-model",
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    block = text.split("---\n", 2)[1]
    result = {}
    for line in block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
    return result


def check_skill(skill_file: Path, errors: list[str]) -> None:
    text = skill_file.read_text(encoding="utf-8")
    meta = frontmatter(text)
    name = meta.get("name")
    if name not in EXPECTED:
        fail(f"unexpected or missing skill name in {skill_file}", errors)
        return
    if set(meta) != {"name", "description"}:
        fail(f"frontmatter must contain only name and description in {skill_file}", errors)
    if len(text.splitlines()) > 500:
        fail(f"skill exceeds the focused-context limit: {skill_file}", errors)
    description = meta.get("description", "")
    has_trigger = "Use when" in description or "Use for" in description
    if len(description) < 80 or not has_trigger or "OAK" not in description:
        fail(f"skill description lacks a specific OAK trigger: {skill_file}", errors)
    if "TODO" in text or "PLACEHOLDER" in text or "\u2014" in text:
        fail(f"placeholder or em dash remains in {skill_file}", errors)
    for resource in re.findall(r"`((?:assets|references|scripts)/[^`\s]+)`", text):
        if not (skill_file.parent / resource).exists():
            fail(f"missing referenced resource {resource} from {skill_file}", errors)

    agent_file = skill_file.parent / "agents/openai.yaml"
    if not agent_file.exists():
        fail(f"missing agents/openai.yaml for {name}", errors)
        return
    agent = agent_file.read_text(encoding="utf-8")
    if "allow_implicit_invocation: true" not in agent:
        fail(f"implicit invocation is not enabled for {name}", errors)
    if f"${name}" not in agent:
        fail(f"default prompt does not reference ${name}", errors)


def check_contracts(errors: list[str]) -> None:
    build = (SKILLS / "luxonis-build/SKILL.md").read_text(encoding="utf-8")
    build_flat = " ".join(build.split())
    for term in (
        "awaiting-user-context",
        "awaiting-plan-approval",
        "$PWD/POC_PLAN.md",
        "contains no unresolved Must-ask decision",
        "authorizes its expected",
        "Do not ask again",
        "persistent shared destination",
        "clearly approved",
        "highest-risk supported assumption",
        "luxonis-inspect-pipeline",
        "working-demo",
        "human-subsystem-required",
    ):
        if term.lower() not in build_flat.lower():
            fail(f"luxonis-build is missing contract: {term}", errors)
    plan = (SKILLS / "luxonis-build/references/plan-poc.md").read_text(encoding="utf-8")
    plan_flat = " ".join(plan.split())
    for term in (
        "Known",
        "Inferable",
        "Must ask",
        "Mermaid",
        "no question limit",
        "A missing artifact does not block planning",
    ):
        if term.lower() not in plan_flat.lower():
            fail(f"plan-poc reference is missing: {term}", errors)
    design = (SKILLS / "luxonis-build/references/design-review.md").read_text(encoding="utf-8")
    for term in ("depth", "crop", "lighting", "FPS", "topology", "queue"):
        if term.lower() not in design.lower():
            fail(f"design review does not route attention to: {term}", errors)
    inspect = (SKILLS / "luxonis-inspect-pipeline/SKILL.md").read_text(encoding="utf-8")
    for term in (
        "oakctl inspect topics",
        "oakctl inspect pipeline",
        "--timeout",
        "never an unnamed positional",
        "explicitly read-only inspection",
        "do not edit source",
    ):
        if term.lower() not in inspect.lower():
            fail(f"inspection contract is missing: {term}", errors)
    setup = (SKILLS / "luxonis-device-setup/SKILL.md").read_text(encoding="utf-8")
    for term in ("create or update `DEVICE.md`", "report-only/read-only"):
        if term.lower() not in setup.lower():
            fail(f"device persistence contract is missing: {term}", errors)
    conversion = (SKILLS / "luxonis-convert-model/SKILL.md").read_text(encoding="utf-8")
    for term in (
        "FP16",
        "INT8",
        "representative",
        "checksum",
        "RVC2",
        "RVC4",
        "archive-metadata-valid-awaiting-inference",
        "metadata gate alone is not archive-ready",
    ):
        if term not in conversion:
            fail(f"conversion contract is missing: {term}", errors)
    integration = (SKILLS / "luxonis-integrate-model/SKILL.md").read_text(encoding="utf-8")
    for term in ("NN Archive", "source of truth", "filtered", "representative"):
        if term.lower() not in integration.lower():
            fail(f"integration contract is missing: {term}", errors)

    removed = {"luxonis-guide", "luxonis-project-interview", "luxonis-plan-poc", "luxonis-build-poc"}
    present = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
    if removed & present:
        fail(f"routing-only or superseded skills remain: {sorted(removed & present)}", errors)


def check_manifests(errors: list[str]) -> None:
    paths = (
        ROOT / ".mcp.json",
        ROOT / ".codex-plugin/plugin.json",
        ROOT / ".claude-plugin/plugin.json",
        ROOT / ".claude-plugin/marketplace.json",
        ROOT / ".cursor-plugin/plugin.json",
        ROOT / "tests/activation_cases.json",
    )
    parsed = {}
    for path in paths:
        try:
            parsed[str(path.relative_to(ROOT))] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            fail(f"invalid JSON {path}: {error}", errors)
    codex = parsed.get(".codex-plugin/plugin.json")
    if codex and (codex.get("skills") != "./skills/" or codex.get("mcpServers") != "./.mcp.json"):
        fail("Codex manifest does not declare both skills and MCP", errors)


def check_scripts(errors: list[str]) -> None:
    scripts = [
        SKILLS / "luxonis-device-setup/scripts/luxonis_doctor.py",
        SKILLS / "luxonis-convert-model/scripts/validate_nn_archive.py",
        ROOT / "tests/fakes/bin/oakctl",
        ROOT / "tests/validate_static.py",
    ]
    with tempfile.TemporaryDirectory(prefix="luxonis-v2-lightweight-pycache-") as cache:
        env = os.environ.copy()
        env["PYTHONPYCACHEPREFIX"] = cache
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", *map(str, scripts)],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
    if result.returncode:
        fail(f"script compilation failed: {result.stderr.strip()}", errors)

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "tests/fakes")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    validator = SKILLS / "luxonis-convert-model/scripts/validate_nn_archive.py"
    result = subprocess.run(
        [
            sys.executable,
            str(validator),
            "--archive",
            str(ROOT / "tests/fixtures/fake_nn_archive.json"),
            "--expected-width", "224",
            "--expected-height", "224",
            "--expected-head-count", "1",
            "--expected-parser", "Classification",
            "--expected-class", "SKU-0042",
            "--expected-class", "SKU-0177",
            "--expected-class", "SKU-9001",
        ],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        fail(f"archive validator fixture failed: {result.stderr.strip()}", errors)


def main() -> int:
    errors: list[str] = []
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    if {path.parent.name for path in skill_files} != EXPECTED:
        fail(f"expected exactly {sorted(EXPECTED)}", errors)
    for skill_file in skill_files:
        check_skill(skill_file, errors)
    check_contracts(errors)
    check_manifests(errors)
    check_scripts(errors)
    if errors:
        print("V2 Lightweight validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"V2 Lightweight validation passed: {len(skill_files)} skills plus no-device fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
