import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "classify_reply.py"
spec = importlib.util.spec_from_file_location("classify_reply", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def test_paid_beats_other_signals():
    result = module.classify(
        "Your submission is approved. Payment has been completed. Transaction hash attached."
    )
    assert result["state"] == "paid"


def test_payment_pending():
    result = module.classify(
        "Your report was accepted and the payout is processing this week."
    )
    assert result["state"] == "payment_pending"


def test_approved():
    result = module.classify("Your submission has been accepted. Great work.")
    assert result["state"] == "approved"


def test_action_required():
    result = module.classify("Could you provide the reproduction logs and confirm the version?")
    assert result["state"] == "action_required"


def test_blocked():
    result = module.classify("Please complete KYC before we can continue.")
    assert result["state"] == "blocked"


def test_waiting_on_generic_ack():
    result = module.classify("Thanks for the update. We will review it.")
    assert result["state"] == "waiting"
