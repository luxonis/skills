#!/usr/bin/env python3
"""Validate NN Archive metadata and classification labels."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import depthai as dai


class ValidationError(ValueError):
    """Raised when archive metadata does not satisfy the requested checks."""


def _head_summary(
    head: dai.nn_archive.v1.Head,
) -> tuple[str, list[str] | None, int | None]:
    parser = head.parser
    if not isinstance(parser, str) or not parser:
        raise ValidationError("head metadata is missing `parser`")

    metadata = head.metadata
    if metadata is None:
        raise ValidationError("head metadata is missing")

    classes = metadata.classes
    class_names = None if classes is None else list(classes)
    n_classes = metadata.nClasses
    if n_classes is not None and class_names is not None:
        if n_classes != len(class_names):
            raise ValidationError(
                f"class count disagrees: nClasses={n_classes}, names={len(class_names)}"
            )
    return parser, class_names, n_classes


def load_archive(args: argparse.Namespace) -> dai.NNArchive:
    if args.archive and args.model_yaml:
        raise ValueError("Use either --archive or --model-yaml, not both.")
    if args.archive:
        return dai.NNArchive(str(args.archive.resolve()))
    if args.model_yaml:
        description = dai.NNModelDescription.fromYamlFile(
            str(args.model_yaml.resolve())
        )
        return dai.NNArchive(dai.getModelFromZoo(description))
    raise ValidationError("provide --archive or --model-yaml")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--archive", type=Path)
    source.add_argument("--model-yaml", type=Path)
    parser.add_argument(
        "--expected-class",
        action="append",
        dest="expected_classes",
        help="Expected class name; repeat in output order.",
    )
    args = parser.parse_args()

    archive = load_archive(args)
    input_size = archive.getInputSize()
    if input_size is None:
        raise ValidationError("archive has no input size")
    width, height = input_size
    config = archive.getConfig()
    model = config.model
    heads = model.heads
    if heads is None or not heads:
        raise ValidationError("model metadata has no heads")

    print(f"input_size={width}x{height}")
    print(f"head_count={len(heads)}")
    for index, head in enumerate(heads):
        parser_name, classes, n_classes = _head_summary(head)
        print(
            f"head[{index}].parser={parser_name} "
            f"classes={classes} n_classes={n_classes}"
        )
        if "classification" in parser_name.lower() and classes is None:
            raise ValidationError(f"head[{index}] classification classes are missing")
        if args.expected_classes is not None:
            if classes is None:
                raise ValidationError(f"head[{index}] expected classes are missing")
            if classes != args.expected_classes:
                raise ValidationError(
                    f"head[{index}] classes disagree: "
                    f"expected={args.expected_classes}, actual={classes}"
                )
            if n_classes is not None and n_classes != len(args.expected_classes):
                raise ValidationError(
                    f"head[{index}] expected class count disagrees: "
                    f"expected={len(args.expected_classes)}, actual={n_classes}"
                )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValidationError, ValueError) as error:
        print(f"archive validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
