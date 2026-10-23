import pytest

from kozphy_sms.core import RULES, analyze, normalize, redact


def test_rules_count():
    assert len(RULES) == 10


def test_high_review_score():
    result = analyze("保證核貸，免聯徵，先付手續費")
    assert result["label"] == "high"
    assert result["score"] >= 50


def test_benign_message():
    assert analyze("明天早上九點開會")["label"] == "low_signal"


def test_warning_negation():
    result = analyze("銀行提醒：請勿提供驗證碼給他人")
    assert not any(item["id"] == "sensitive" for item in result["matched_rules"])


def test_broker_advertisement_not_automatically_fraud():
    result = analyze("代辦銀行借款，免押保，300萬")
    assert result["is_fraud_probability"] is False
    assert result["label"] == "review"


def test_phone_and_email_redaction():
    redacted = redact("請聯絡 0912-345-678 或 test@example.com")
    assert "[PHONE]" in redacted
    assert "[EMAIL]" in redacted
    assert "0912" not in redacted


def test_nfkc_normalization():
    assert normalize("ＡＢＣ") == "abc"


def test_non_string_error():
    with pytest.raises(TypeError):
        analyze(None)
