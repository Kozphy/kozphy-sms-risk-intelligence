"""Interpretable SMS triage rules. Scores are not fraud probabilities."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict, dataclass

PHONE = re.compile(r"(?<!\d)(?:\+?886[- ]?)?0?9\d{2}[- ]?\d{3}[- ]?\d{3}(?!\d)")
EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
SAFE_WARNING = re.compile(
    r"(?:請勿|不要|切勿|不可|請不要|勿|禁止).{0,10}"
    r"(?:提供|透露|告知|分享).{0,8}(?:驗證碼|密碼|otp)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Rule:
    id: str
    pattern: str
    weight: int
    reason: str


RULES = (
    Rule("guarantee", r"保證(?:過件|核貸|撥款)", 25, "Guarantee claim"),
    Rule("no_checks", r"免(?:審核|聯徵)", 20, "No credit checks claim"),
    Rule("upfront_fee", r"(?:先付|預付).{0,6}(?:手續費|保證金)", 35, "Upfront fee"),
    Rule("sensitive", r"(?:提供|告知|傳送).{0,8}(?:密碼|驗證碼|otp)", 45, "Sensitive credentials request"),
    Rule("no_collateral", r"免押保", 10, "No collateral claim"),
    Rule("fast_funds", r"(?:快速|立即|當日)撥款", 10, "Fast funding claim"),
    Rule("urgent", r"(?:馬上服務|立即聯絡)", 5, "Urgency wording"),
    Rule("broker", r"代辦", 10, "Loan brokerage"),
    Rule("large_loan", r"(?:250|300)萬", 5, "Large loan advertisement"),
    Rule("check_loan", r"(?:支票借款|借支票)", 15, "Cheque-backed lending"),
)


def normalize(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("SMS text must be a string")
    return unicodedata.normalize("NFKC", text).casefold().strip()


def redact(text: str) -> str:
    return EMAIL.sub("[EMAIL]", PHONE.sub("[PHONE]", text))


def analyze(text: str) -> dict:
    normalized = normalize(text)
    warning = bool(SAFE_WARNING.search(normalized))
    matched = []
    for rule in RULES:
        if rule.id == "sensitive" and warning:
            continue  # Narrow mitigation; warnings can still contain other risky content.
        if re.search(rule.pattern, normalized, re.IGNORECASE):
            matched.append({"id": rule.id, "reason": rule.reason, "weight": rule.weight})
    score = min(100, sum(m["weight"] for m in matched))
    label = "high" if score >= 50 else "review" if score >= 20 else "low_signal"
    return {
        "score": score,
        "label": label,
        "matched_rules": matched,
        "redacted_text": redact(text),
        "model": "rules-v0.1",
        "is_fraud_probability": False,
    }


def rules() -> list[dict]:
    return [asdict(rule) for rule in RULES]
