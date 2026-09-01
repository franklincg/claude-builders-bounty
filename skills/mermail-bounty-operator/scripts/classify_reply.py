#!/usr/bin/env python3
"""Deterministic helper for demoing Mermail Bounty Operator state transitions.

Input: one JSON object on stdin with optional subject/body fields.
Output: one JSON object with state, confidence, and matched signals.

This helper intentionally does not click links, send mail, inspect secrets, or make
network requests. It is a conservative first-pass classifier; the agent must verify
important transitions against the actual Mermail message/thread evidence.
"""

from __future__ import annotations

import json
import re
import sys

RULES = [
    (
        "paid",
        0.90,
        [
            r"\bpayment (?:has been )?(?:completed|settled|received)\b",
            r"\bpayout (?:has been )?(?:completed|sent|settled)\b",
            r"\btransaction (?:id|hash)\b",
            r"\breceipt\b.*\b(?:paid|settled)\b",
        ],
    ),
    (
        "payment_pending",
        0.82,
        [
            r"\b(?:approved|accepted|winner|awarded)\b.*\b(?:payment|payout|invoice)\b",
            r"\bpayment (?:is )?(?:pending|processing|scheduled)\b",
            r"\bpayout (?:is )?(?:pending|processing|scheduled)\b",
        ],
    ),
    (
        "approved",
        0.82,
        [
            r"\b(?:you(?:'|’)re|you are) (?:the )?(?:winner|selected|approved|accepted)\b",
            r"\b(?:submission|report|work|proposal) (?:is|was|has been) (?:approved|accepted)\b",
            r"\bwe(?:'|’)d like to (?:hire|award|proceed with)\b",
        ],
    ),
    (
        "rejected",
        0.86,
        [
            r"\b(?:submission|report|proposal) (?:is|was|has been) (?:rejected|declined|invalid)\b",
            r"\b(?:duplicate|not selected|no award|won(?:'|’)t be moving forward)\b",
        ],
    ),
    (
        "blocked",
        0.78,
        [
            r"\b(?:complete|finish|pass) kyc\b",
            r"\bwallet (?:signature|signing|approval)\b",
            r"\b(?:deposit|pay|purchase) .{0,20}(?:fee|funds|usdc|usd|sol)\b",
            r"\b(?:sign in|login|captcha)\b",
            r"\bprivate (?:repo|repository|access|credential)\b",
        ],
    ),
    (
        "action_required",
        0.70,
        [
            r"\bplease (?:update|revise|clarify|provide|send|share|fix|confirm)\b",
            r"\bcould you (?:update|revise|clarify|provide|send|share|fix|confirm)\b",
            r"\bneed (?:more|additional) (?:details|evidence|information)\b",
        ],
    ),
]


def classify(text: str) -> dict:
    normalized = " ".join(text.lower().split())
    matches = []
    for state, confidence, patterns in RULES:
        for pattern in patterns:
            if re.search(pattern, normalized, flags=re.I):
                matches.append({"state": state, "confidence": confidence, "signal": pattern})
                break

    if not matches:
        return {"state": "waiting", "confidence": 0.55, "matchedSignals": []}

    # RULES are ordered by operational precedence; take the first matched state.
    winner = matches[0]
    return {
        "state": winner["state"],
        "confidence": winner["confidence"],
        "matchedSignals": [m["state"] for m in matches],
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        print(json.dumps({"error": f"invalid_json: {exc}"}))
        return 2

    subject = str(payload.get("subject") or "")
    body = str(payload.get("body") or "")
    result = classify(f"{subject}\n{body}")
    result["requiresEvidenceVerification"] = result["state"] in {
        "approved",
        "payment_pending",
        "paid",
        "rejected",
        "blocked",
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
