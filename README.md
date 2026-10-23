# Kozphy SMS Risk Intelligence

An explainable, privacy-conscious **rule-based baseline** for reviewing suspicious loan advertising SMS. Not a fraud probability model, legal determination, or production-ready service.

## Features
- Unicode NFKC normalization and 10 interpretable signals
- Explicit handling of "do not share OTP" warnings to reduce false positives
- Redaction of phone numbers and email addresses in returned text
- Local CLI, CSV-to-JSONL batch export, optional FastAPI endpoint
- Synthetic labeled evaluation set; pytest and Ruff CI

## Quick start

```bash
python -m pip install -e ".[dev,api]"
pytest -q
ruff check .
python -m kozphy_sms.cli analyze "代辦貸款，快速撥款，免押保"
python -m kozphy_sms.eval
uvicorn kozphy_sms.api:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs for local API documentation.

## Batch analysis

Create a UTF-8 CSV containing a `text` column.

```bash
python -m kozphy_sms.cli batch input.csv output.jsonl
```

Results intentionally **do not store raw SMS**. Review source data permissions and local retention practices before using real messages.

## What the score means

The score is an **uncalibrated review-priority heuristic** from 0–100. It is *not* an estimate of fraud likelihood. Loan advertising alone is not evidence of crime; negative warnings are not proof of safety.

## Evaluation

`python -m kozphy_sms.eval` reports a confusion matrix, precision, recall and F1 using only a **tiny synthetic** benchmark. These metrics must not be advertised as real-world fraud detection accuracy. For deployment, obtain lawful, representative, de-identified data and independent human labeling.

## Safety and limitations

Do not publish third-party phone numbers, individual sender names, or unredacted SMS. Avoid automatically accusing a sender of fraud. The API has no authentication or throttling: bind locally only. See [roadmap](docs/ROADMAP.md).

MIT licensed.
