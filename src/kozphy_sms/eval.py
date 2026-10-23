"""Evaluate the triage baseline on *synthetic* labeled data only."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .core import analyze

DATASET = Path(__file__).resolve().parents[2] / "data" / "eval_synthetic.csv"


def evaluate(path: Path = DATASET) -> dict:
    tp = fp = tn = fn = 0
    with path.open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            actual = int(row["needs_review"])
            predicted = int(analyze(row["text"])["label"] != "low_signal")
            tp += int(actual == 1 and predicted == 1)
            fp += int(actual == 0 and predicted == 1)
            tn += int(actual == 0 and predicted == 0)
            fn += int(actual == 1 and predicted == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "dataset": "synthetic-only",
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
