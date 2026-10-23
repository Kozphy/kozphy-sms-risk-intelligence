from kozphy_sms.eval import evaluate


def test_metrics_within_range():
    metrics = evaluate()
    assert metrics["dataset"] == "synthetic-only"
    assert sum(metrics[key] for key in ("tp", "fp", "tn", "fn")) == 12
    for key in ("precision", "recall", "f1"):
        assert 0 <= metrics[key] <= 1
