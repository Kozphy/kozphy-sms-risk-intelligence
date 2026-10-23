"""Command line interface for analysis and local CSV batch jobs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .core import analyze


def main() -> None:
    parser = argparse.ArgumentParser(description="Kozphy SMS triage baseline")
    sub = parser.add_subparsers(dest="command", required=True)
    single = sub.add_parser("analyze")
    single.add_argument("text")
    batch = sub.add_parser("batch")
    batch.add_argument("input_csv", type=Path)
    batch.add_argument("output_jsonl", type=Path)
    args = parser.parse_args()
    if args.command == "analyze":
        print(json.dumps(analyze(args.text), ensure_ascii=False, indent=2))
        return
    with args.input_csv.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or "text" not in reader.fieldnames:
            parser.error("Input CSV must include a text column")
        with args.output_jsonl.open("w", encoding="utf-8") as target:
            for row in reader:
                result = analyze(row.get("text") or "")
                target.write(json.dumps(result, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
