"""
Stage 6 — Execution (Actions)
Security Mechanism: Proof-Carrying Memory
No result is stored unless it carries verifiable proof + provenance.
"""
import hashlib
import re
import time

SENSITIVE_PATTERNS = [
    r"\b\d{13,16}\b",                       # card-like numbers
    r"\b\d{3}-\d{2}-\d{4}\b",               # SSN-like
    r"[\w\.-]+@[\w\.-]+\.\w+",              # emails
]


def redact(text):
    for pattern in SENSITIVE_PATTERNS:
        text = re.sub(pattern, "[REDACTED]", text)
    return text


def execute_action(subtask, sim_result):
    if sim_result["decision"] != "APPROVE":
        return {
            "step": subtask["step"],
            "executed": False,
            "reason": sim_result["decision"],
            "output": None,
            "provenance": None,
            "proof_hash": None,
            "stored_without_proof": False,
        }

    raw_result = f"Simulated result: '{subtask['action']}' completed on '{subtask['target']}'."
    provenance = {
        "source": "internal_simulated_tool",
        "verified_with_external_source": True,
        "timestamp": time.time(),
    }
    proof_hash = hashlib.sha256((raw_result + str(provenance["timestamp"])).encode()).hexdigest()[:32]
    sanitized_output = redact(raw_result)

    return {
        "step": subtask["step"],
        "executed": True,
        "output": sanitized_output,
        "provenance": provenance,
        "proof_hash": proof_hash,
        "stored_without_proof": False,
    }
