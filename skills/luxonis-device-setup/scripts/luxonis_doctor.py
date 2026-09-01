#!/usr/bin/env python3
"""Report non-destructive host facts relevant to Luxonis development."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from typing import Any


def command_version(command: str, args: list[str]) -> dict[str, Any]:
    path = shutil.which(command)
    if path is None:
        return {"available": False, "path": None, "output": None}
    try:
        result = subprocess.run(
            [path, *args], check=False, capture_output=True, text=True, timeout=10
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"available": True, "path": path, "output": None, "error": str(error)}
    output = (result.stdout or result.stderr).strip().splitlines()
    return {
        "available": True,
        "path": path,
        "exit_code": result.returncode,
        "output": output[0] if output else "",
    }


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def collect() -> dict[str, Any]:
    return {
        "host": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "python": {
            "executable": sys.executable,
            "version": platform.python_version(),
            "virtual_environment": sys.prefix != getattr(sys, "base_prefix", sys.prefix),
        },
        "packages": {
            "depthai": package_version("depthai"),
            "depthai-nodes": package_version("depthai-nodes"),
        },
        "commands": {
            "oakctl": command_version("oakctl", ["--version"]),
            "adb": command_version("adb", ["version"]),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "text"), default="text")
    args = parser.parse_args()
    facts = collect()
    if args.format == "json":
        print(json.dumps(facts, indent=2, sort_keys=True))
    else:
        print(f"host={facts['host']['system']} {facts['host']['release']} {facts['host']['machine']}")
        print(f"python={facts['python']['version']} executable={facts['python']['executable']}")
        print(f"virtual_environment={facts['python']['virtual_environment']}")
        print(f"depthai={facts['packages']['depthai'] or 'not installed'}")
        print(f"depthai_nodes={facts['packages']['depthai-nodes'] or 'not installed'}")
        print(f"oakctl={facts['commands']['oakctl']['output'] or 'not available'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
