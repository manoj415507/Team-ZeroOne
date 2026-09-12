"""
Stage 6 (Memory Update)
Security Mechanism: Memory Trust Score
"""
import time


def score_memory(exec_result):
    if not exec_result.get("executed"):
        return {
            "step": exec_result["step"],
            "trust_score": 0,
            "stored": False,
            "reason": exec_result.get("reason"),
        }

    age_seconds = max(time.time() - exec_result["provenance"]["timestamp"], 0)
    freshness_score = 100 if age_seconds < 5 else max(100 - int(age_seconds), 0)
    provenance_ok = exec_result["provenance"]["verified_with_external_source"]

    trust_score = round((0.6 * (100 if provenance_ok else 30)) + (0.4 * freshness_score))

    return {
        "step": exec_result["step"],
        "trust_score": trust_score,
        "provenance_verified": provenance_ok,
        "freshness_score": freshness_score,
        "stored": True,
        "redacted_before_store": True,
    }
