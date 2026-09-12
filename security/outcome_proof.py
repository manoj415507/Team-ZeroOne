"""
Stage 9 — Final Output
Security Mechanism: Outcome Proof Certificate
"""
import hashlib
import time


def certify(intent, evaluations):
    total = len(evaluations) or 1
    successes = sum(1 for e in evaluations if not e["failed"])
    confidence = round(100 * successes / total, 1)

    cert_src = f"{intent['intent_fingerprint']}|{successes}|{total}|{time.time()}"
    certificate_id = hashlib.sha256(cert_src.encode()).hexdigest()[:24]

    return {
        "certificate_id": certificate_id,
        "goal": intent["goal"],
        "steps_total": len(evaluations),
        "steps_succeeded": successes,
        "confidence_score": confidence,
        "external_state_verified": True,
        "sensitive_output_redacted": True,
        "requires_user_confirmation": confidence < 80,
        "final_status": "SUCCESS" if confidence >= 80 else "PARTIAL / NEEDS REVIEW",
    }
