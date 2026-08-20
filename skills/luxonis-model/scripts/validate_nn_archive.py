#!/usr/bin/env python3
"""Validate DepthAI NN Archive input and head metadata.

Adapted from the experimental Luxonis custom-model harness at commit
d455d573aa7f9ef4d96753f060f9e77859441b80.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


class ValidationError(ValueError):
    """Raised when archive metadata does not satisfy requested checks."""


def load_depthai() -> Any:
    try:
        import depthai as dai
    except ImportError as error:
        raise ValidationError(
            "depthai is not installed in this environment; use the conversion environment"
        ) from error
    return dai


def load_archive(args: argparse.Namespace) -> Any:
    dai = load_depthai()
    if args.archive:
        return dai.NNArchive(str(args.archive.resolve()))
    description = dai.NNModelDescription.fromYamlFile(str(args.model_yaml.resolve()))
    return dai.NNArchive(dai.getModelFromZoo(description))


def head_summary(head: Any) -> tuple[str, list[str] | None, int | None]:
    parser_name = head.parser
    if not isinstance(parser_name, str) or not parser_name:
        raise ValidationError("head metadata is missing `parser`")
    metadata = head.metadata
    if metadata is None:
        raise ValidationError("head metadata is missing")
    classes = metadata.classes
    class_names = None if classes is None else list(classes)
    n_classes = metadata.nClasses
    if n_classes is not None and class_names is not None and n_classes != len(class_names):
        raise ValidationError(
            f"class count disagrees: nClasses={n_classes}, names={len(class_names)}"
        )
    return parser_name, class_names, n_classes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--archive", type=Path)
    source.add_argument("--model-yaml", type=Path)
    parser.add_argument("--expected-width", type=int)
    parser.add_argument("--expected-height", type=int)
    parser.add_argument("--expected-head-count", type=int)
    parser.add_argument("--head-index", type=int, default=0)
    parser.add_argument("--expected-parser")
    parser.add_argument(
        "--expected-class",
        action="append",
        dest="expected_classes",
        help="Expected class name for the selected head; repeat in output order.",
    )
    args = parser.parse_args()

    archive = load_archive(args)
    input_size = archive.getInputSize()
    if input_size is None:
        raise ValidationError("archive has no input size")
    width, height = input_size
    if args.expected_width is not None and width != args.expected_width:
        raise ValidationError(f"input width disagrees: expected={args.expected_width}, actual={width}")
    if args.expected_height is not None and height != args.expected_height:
        raise ValidationError(
            f"input height disagrees: expected={args.expected_height}, actual={height}"
        )

    heads = archive.getConfig().model.heads
    if heads is None or not heads:
        raise ValidationError("model metadata has no heads")
    if args.expected_head_count is not None and len(heads) != args.expected_head_count:
        raise ValidationError(
            f"head count disagrees: expected={args.expected_head_count}, actual={len(heads)}"
        )
    if args.head_index < 0 or args.head_index >= len(heads):
        raise ValidationError(f"head index {args.head_index} is outside 0..{len(heads) - 1}")

    print(f"input_size={width}x{height}")
    print(f"head_count={len(heads)}")
    for index, head in enumerate(heads):
        parser_name, classes, n_classes = head_summary(head)
        print(f"head[{index}].parser={parser_name} classes={classes} n_classes={n_classes}")

    parser_name, classes, n_classes = head_summary(heads[args.head_index])
    if args.expected_parser is not None and parser_name != args.expected_parser:
        raise ValidationError(
            f"head[{args.head_index}] parser disagrees: "
            f"expected={args.expected_parser}, actual={parser_name}"
        )
    if "classification" in parser_name.lower() and classes is None:
        raise ValidationError(f"head[{args.head_index}] classification classes are missing")
    if args.expected_classes is not None:
        if classes != args.expected_classes:
            raise ValidationError(
                f"head[{args.head_index}] classes disagree: "
                f"expected={args.expected_classes}, actual={classes}"
            )
        if n_classes is not None and n_classes != len(args.expected_classes):
            raise ValidationError(
                f"head[{args.head_index}] expected class count disagrees: "
                f"expected={len(args.expected_classes)}, actual={n_classes}"
            )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValidationError, ValueError) as error:
        print(f"archive validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
