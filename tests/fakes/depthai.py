"""Minimal DepthAI metadata fake for the NN Archive validator."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace


class NNArchive:
    def __init__(self, source):
        data = json.loads(Path(source).read_text(encoding="utf-8"))
        self._input_size = tuple(data["input_size"])
        heads = []
        for item in data["heads"]:
            metadata = SimpleNamespace(
                classes=item.get("classes"),
                nClasses=item.get("nClasses"),
            )
            heads.append(SimpleNamespace(parser=item.get("parser"), metadata=metadata))
        self._config = SimpleNamespace(model=SimpleNamespace(heads=heads))

    def getInputSize(self):
        return self._input_size

    def getConfig(self):
        return self._config


class NNModelDescription:
    @staticmethod
    def fromYamlFile(path):
        return path


def getModelFromZoo(description):
    return description
