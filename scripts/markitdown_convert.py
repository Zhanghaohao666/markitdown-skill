#!/usr/bin/env python3
"""Batch and advanced conversion wrapper for Microsoft MarkItDown."""

from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme.lower() in {"http", "https"} and bool(parsed.netloc)


def split_csv(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def expand_sources(values: list[str], recursive: bool, include: list[str] | None) -> list[str]:
    sources: list[str] = []
    include = include or ["*"]

    for value in values:
        if is_url(value):
            sources.append(value)
            continue

        path = Path(value)
        if path.is_dir():
            iterator = path.rglob("*") if recursive else path.glob("*")
            for candidate in iterator:
                if candidate.is_file() and any(candidate.match(pattern) for pattern in include):
                    sources.append(str(candidate))
            continue

        matches = glob.glob(value, recursive=recursive)
        if matches:
            sources.extend(str(Path(match)) for match in matches if Path(match).is_file())
        else:
            sources.append(value)

    seen: set[str] = set()
    unique: list[str] = []
    for source in sources:
        key = source if is_url(source) else str(Path(source).resolve())
        if key not in seen:
            seen.add(key)
            unique.append(source)
    return unique


def output_name_for(source: str) -> str:
    if is_url(source):
        parsed = urlparse(source)
        base = Path(parsed.path.rstrip("/")).stem or parsed.netloc
    else:
        base = Path(source).stem
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", base).strip("-._")
    return f"{base or 'document'}.md"


def content_from_result(result: object) -> str:
    for attr in ("text_content", "markdown", "text"):
        value = getattr(result, attr, None)
        if value is not None:
            return str(value)
    return str(result)


def build_markitdown(args: argparse.Namespace):
    try:
        from markitdown import MarkItDown
    except ImportError as exc:
        raise SystemExit(
            "MarkItDown is not installed. Install it with: "
            "python -m pip install -U \"markitdown[all]\""
        ) from exc

    kwargs: dict[str, object] = {"enable_plugins": args.use_plugins}

    if args.llm_model:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise SystemExit(
                "The OpenAI Python package is required for --llm-model. "
                "Install it with: python -m pip install -U openai"
            ) from exc
        kwargs["llm_client"] = OpenAI()
        kwargs["llm_model"] = args.llm_model
        if args.llm_prompt:
            kwargs["llm_prompt"] = args.llm_prompt

    if args.docintel_endpoint:
        kwargs["docintel_endpoint"] = args.docintel_endpoint

    if args.cu_endpoint:
        kwargs["cu_endpoint"] = args.cu_endpoint
    if args.cu_analyzer_id:
        kwargs["cu_analyzer_id"] = args.cu_analyzer_id
    if args.cu_file_types:
        try:
            from markitdown.converters import ContentUnderstandingFileType
        except ImportError as exc:
            raise SystemExit(
                "--cu-file-types requires MarkItDown Content Understanding support. "
                "Install with: python -m pip install -U \"markitdown[az-content-understanding]\""
            ) from exc
        selected = []
        for item in split_csv(args.cu_file_types) or []:
            name = item.upper().replace("-", "_")
            try:
                selected.append(getattr(ContentUnderstandingFileType, name))
            except AttributeError as exc:
                raise SystemExit(f"Unknown Content Understanding file type: {item}") from exc
        kwargs["cu_file_types"] = selected

    return MarkItDown(**kwargs)


def convert_one(md, source: str, local_only: bool) -> str:
    if local_only:
        if is_url(source):
            raise ValueError(f"--local-only refuses remote source: {source}")
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(source)
        if hasattr(md, "convert_local"):
            return content_from_result(md.convert_local(str(path)))
    return content_from_result(md.convert(source))


def write_output(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists; pass --overwrite to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert files, directories, globs, or URLs to Markdown with MarkItDown."
    )
    parser.add_argument("sources", nargs="+", help="Files, directories, globs, or http(s) URLs.")
    parser.add_argument("-o", "--output", help="Output file for a single source.")
    parser.add_argument("--output-dir", help="Directory for one Markdown file per source.")
    parser.add_argument("--stdout", action="store_true", help="Write converted Markdown to stdout.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing output files.")
    parser.add_argument("--recursive", action="store_true", help="Recurse into directories or ** globs.")
    parser.add_argument(
        "--include",
        action="append",
        help="Directory include glob, repeatable. Example: --include '*.pdf' --include '*.docx'",
    )
    parser.add_argument("--local-only", action="store_true", help="Refuse remote URLs and use local conversion when available.")
    parser.add_argument("--use-plugins", action="store_true", help="Enable installed MarkItDown plugins.")
    parser.add_argument("--llm-model", help="LLM model for image descriptions or compatible plugins.")
    parser.add_argument("--llm-prompt", help="Optional prompt for LLM image descriptions.")
    parser.add_argument("--docintel-endpoint", help="Azure Document Intelligence endpoint.")
    parser.add_argument("--cu-endpoint", help="Azure Content Understanding endpoint.")
    parser.add_argument("--cu-analyzer-id", help="Azure Content Understanding analyzer id.")
    parser.add_argument("--cu-file-types", help="Comma-separated CU file types, such as PDF,DOCX.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    sources = expand_sources(args.sources, args.recursive, args.include)

    if not sources:
        print("No sources matched.", file=sys.stderr)
        return 2
    if args.output and len(sources) != 1:
        print("--output can only be used with one source.", file=sys.stderr)
        return 2
    if len(sources) > 1 and not (args.output_dir or args.stdout):
        print("Multiple sources require --output-dir or --stdout.", file=sys.stderr)
        return 2

    md = build_markitdown(args)
    failures = 0

    for index, source in enumerate(sources, start=1):
        try:
            content = convert_one(md, source, args.local_only)
            if args.stdout or (not args.output and not args.output_dir):
                if len(sources) > 1:
                    print(f"\n<!-- markitdown source: {source} -->\n")
                print(content)
                continue

            target = Path(args.output) if args.output else Path(args.output_dir) / output_name_for(source)
            write_output(target, content, args.overwrite)
            print(f"[{index}/{len(sources)}] wrote {target}", file=sys.stderr)
        except Exception as exc:  # noqa: BLE001 - keep batch conversion moving.
            failures += 1
            print(f"[{index}/{len(sources)}] failed {source}: {exc}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
