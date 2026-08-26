#!/usr/bin/env python3
"""Deterministic structure and no-device checks for the Luxonis skills."""

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
    "luxonis",
    "luxonis-app",
    "luxonis-workspace",
    "luxonis-device-setup",
    "luxonis-record",
    "luxonis-inspect",
    "luxonis-troubleshoot",
    "luxonis-model",
}
REMOVED = {
    "luxonis-guide",
    "luxonis-project-interview",
    "luxonis-plan-poc",
    "luxonis-build-poc",
    "luxonis-build",
    "luxonis-convert-model",
    "luxonis-integrate-model",
    "luxonis-inspect-pipeline",
}

# Canonical lines duplicated per skill (skills stay self-contained for per-skill installs).
# Compared whitespace-normalized so wrapping may differ; wording may not.
CANON_FACTS = (
    "Best source first: the Luxonis MCP `code` tool, then the exact example or doc source "
    "it returns, then `https://docs.luxonis.com/llms.txt`, then installed CLI `--help`, "
    "then observed behavior; memory is only for general reasoning. If observed host or "
    "device behavior contradicts docs or MCP, trust the observation and note the conflict. "
    "If offline, work from installed `--help` and local examples and name which facts are "
    "unverified."
)
CANON_RUNNER = (
    "Prefer `oakctl run-script` for host runs when installed `--help` lists it as a local "
    "DepthAI environment runner; do not invent subcommands. If no host runner exists, run "
    "via the project env and still use oakctl for inspect and udev."
)
# The harness-prefixed MCP tool name differs per host (and per install mode); skills must
# name the server's native `code` tool instead of hardcoding one host's form.
BANNED_TOOL_NAME = "luxonis__code"


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


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
    if name != skill_file.parent.name or name not in EXPECTED:
        fail(f"unexpected or missing skill name in {skill_file}", errors)
        return
    if set(meta) != {"name", "description"}:
        fail(f"frontmatter must contain only name and description in {skill_file}", errors)
    if not meta.get("description"):
        fail(f"missing description in {skill_file}", errors)
    if len(text.splitlines()) > 500:
        fail(f"skill exceeds the focused-context limit: {skill_file}", errors)
    if "TODO" in text or "PLACEHOLDER" in text:
        fail(f"placeholder remains in {skill_file}", errors)
    for resource in re.findall(r"`((?:assets|references|scripts)/[^`\s]+)`", text):
        if not (skill_file.parent / resource).exists():
            fail(f"missing referenced resource {resource} from {skill_file}", errors)

    flat = normalized(text)
    if CANON_FACTS not in flat:
        fail(f"canonical fact-source ladder missing or drifted in {skill_file}", errors)
    if "run-script" in text and CANON_RUNNER not in flat:
        fail(f"canonical host-runner line missing or drifted in {skill_file}", errors)

    agent_file = skill_file.parent / "agents/openai.yaml"
    if not agent_file.exists():
        fail(f"missing agents/openai.yaml for {name}", errors)
        return
    agent = agent_file.read_text(encoding="utf-8")
    if "allow_implicit_invocation: true" not in agent:
        fail(f"implicit invocation is not enabled for {name}", errors)
    if f"${name}" not in agent:
        fail(f"default prompt does not reference ${name}", errors)
    if 'value: "luxonis"' not in agent or "https://mcp.luxonis.com/mcp" not in agent:
        fail(f"MCP dependency is missing for {name}", errors)


def check_no_hardcoded_tool_name(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        if BANNED_TOOL_NAME in path.read_text(encoding="utf-8"):
            fail(
                f"hardcoded MCP tool name `{BANNED_TOOL_NAME}` in {path};"
                " name the Luxonis MCP `code` tool instead",
                errors,
            )


def check_layout(errors: list[str]) -> None:
    present = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
    if present != EXPECTED:
        fail(f"expected exactly {sorted(EXPECTED)}, found {sorted(present)}", errors)
    leftover = REMOVED & present
    if leftover:
        fail(f"superseded skills remain: {sorted(leftover)}", errors)
    if (SKILLS / "building").exists():
        fail("empty leftover skills/building/ remains", errors)


def check_manifests(errors: list[str]) -> None:
    paths = (
        ROOT / "plugin.json",
        ROOT / "mcp.json",
        ROOT / ".mcp.json",
        ROOT / ".claude-plugin/plugin.json",
        ROOT / ".claude-plugin/marketplace.json",
        ROOT / "tests/activation_cases.json",
    )
    parsed: dict[str, object] = {}
    for path in paths:
        try:
            parsed[str(path.relative_to(ROOT))] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            fail(f"invalid JSON {path}: {error}", errors)
    for key in (
        "plugin.json",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
    ):
        data = parsed.get(key)
        if not isinstance(data, dict):
            continue
        name = data.get("name")
        if name != "luxonis":
            fail(f"{key} plugin identity is {name!r}, expected luxonis", errors)
        if "v2-draft" in json.dumps(data):
            fail(f"{key} still references v2-draft", errors)

    # Portable Agent Plugins manifests (https://agent-plugins.org) serve Codex, Cursor, and
    # other standard hosts; .claude-plugin/ plus .mcp.json remain for Claude Code.
    for legacy in (".codex-plugin", ".cursor-plugin"):
        if (ROOT / legacy).exists():
            fail(f"legacy host manifest {legacy}/ remains; the root plugin.json replaces it", errors)
    portable = parsed.get("plugin.json")
    if isinstance(portable, dict):
        if portable.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            fail("plugin.json is missing the Agent Plugins 1.0.0 $schema", errors)
        extensions = portable.get("extensions")
        codex_interface = (
            extensions.get("com.openai", {}).get("interface") if isinstance(extensions, dict) else None
        )
        if not isinstance(codex_interface, dict):
            fail("plugin.json is missing the com.openai interface extension", errors)
    portable_mcp = parsed.get("mcp.json")
    if isinstance(portable_mcp, dict):
        server = portable_mcp.get("mcpServers", {}).get("luxonis", {})
        if portable_mcp.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json":
            fail("mcp.json is missing the Agent Plugins 1.0.0 mcp $schema", errors)
        if server.get("type") != "streamable-http" or server.get("url") != "https://mcp.luxonis.com/mcp":
            fail("mcp.json does not declare the luxonis streamable-http server", errors)
    claude_mcp = parsed.get(".mcp.json")
    if isinstance(claude_mcp, dict):
        claude_url = claude_mcp.get("mcpServers", {}).get("luxonis", {}).get("url")
        if claude_url != "https://mcp.luxonis.com/mcp":
            fail(".mcp.json does not declare the luxonis server for Claude Code", errors)


def check_scripts(errors: list[str]) -> None:
    scripts = [
        SKILLS / "luxonis-device-setup/scripts/luxonis_doctor.py",
        SKILLS / "luxonis-model/scripts/validate_nn_archive.py",
        SKILLS / "luxonis-record/scripts/holistic_record.py",
        ROOT / "tests/fakes/bin/oakctl",
        ROOT / "tests/validate_static.py",
    ]
    missing = [str(path) for path in scripts if not path.exists()]
    if missing:
        fail(f"missing scripts: {missing}", errors)
        return
    with tempfile.TemporaryDirectory(prefix="luxonis-skills-pycache-") as cache:
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
    validator = SKILLS / "luxonis-model/scripts/validate_nn_archive.py"
    result = subprocess.run(
        [
            sys.executable,
            str(validator),
            "--archive",
            str(ROOT / "tests/fixtures/fake_nn_archive.json"),
            "--expected-width",
            "224",
            "--expected-height",
            "224",
            "--expected-head-count",
            "1",
            "--expected-parser",
            "Classification",
            "--expected-class",
            "SKU-0042",
            "--expected-class",
            "SKU-0177",
            "--expected-class",
            "SKU-9001",
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
    check_layout(errors)
    check_no_hardcoded_tool_name(errors)
    for skill_file in sorted(SKILLS.glob("*/SKILL.md")):
        check_skill(skill_file, errors)
    check_manifests(errors)
    check_scripts(errors)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    skill_count = len(list(SKILLS.glob("*/SKILL.md")))
    print(f"Validation passed: {skill_count} skills plus no-device fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
