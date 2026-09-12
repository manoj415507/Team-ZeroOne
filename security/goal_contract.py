"""
Stage 3 — Goal Contract / Intent Lock
Security Mechanism: Goal Contract / Intent Lock
"""

ALLOWED_ACTIONS = ["create", "read", "search", "analyze", "generate", "update",
                    "schedule", "fetch", "book", "share", "install"]
DISALLOWED_ACTIONS = ["delete", "transfer", "wire", "format", "drop table",
                       "shutdown", "bypass", "override", "pay", "remove"]


def build_contract(intent):
    allowed = [a for a in intent["actions"] if a in ALLOWED_ACTIONS]
    blocked = [a for a in intent["actions"] if a not in ALLOWED_ACTIONS]

    limits = {
        "max_cost_usd": 5.0,
        "max_actions": 8,
        "data_access": "read-only" if intent["risk_level"] != "LOW" else "read-write",
    }

    enforced = len(blocked) == 0
    return {
        "allowed_actions": allowed or ["analyze"],
        "blocked_actions": blocked,
        "limits": limits,
        "enforced": enforced,
        "policy_decision": "ALLOW" if enforced else "PARTIAL_BLOCK",
    }
