"""
Stage 5 — Tool Selection
Security Mechanism: Action Shadow Simulation (sandboxed dry-run before real execution)
"""
import random


def simulate(subtask):
    # deterministic pseudo-randomness so demo results are stable per action/target
    seed = abs(hash(subtask["action"] + subtask["target"])) % (2 ** 32)
    rng = random.Random(seed)

    param_drift = rng.random() < 0.08
    base_risk = rng.randint(1, 100) if subtask["permission_budget"]["write"] else rng.randint(1, 40)

    decision = "APPROVE"
    if base_risk > 75:
        decision = "ESCALATE_HUMAN_APPROVAL"
    elif param_drift:
        decision = "BLOCK_PARAM_DRIFT"

    return {
        "step": subtask["step"],
        "action": subtask["action"],
        "target": subtask["target"],
        "sandboxed": True,
        "param_drift_detected": param_drift,
        "risk_score": base_risk,
        "decision": decision,
    }
