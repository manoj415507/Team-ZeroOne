"""
Stage 2 — Intent Understanding
Security Mechanism: Intent DNA Fingerprint
"""
import hashlib
import re

RISK_KEYWORDS = {
    "delete": 40, "remove": 30, "transfer": 50, "wire": 60, "password": 70,
    "credit card": 80, "ssn": 90, "admin": 35, "sudo": 45, "drop table": 90,
    "shutdown": 55, "format": 60, "bypass": 65, "override": 40, "hack": 70,
}

ACTION_WORDS = r"\b(create|delete|update|send|transfer|read|write|search|fetch|remove|book|schedule|analyze|generate|deploy|install|pay|share)\b"
TARGET_WORDS = r"\b(file|email|account|database|server|payment|document|report|calendar|ticket|user|record|invoice|order)s?\b"
DATA_WORDS = r"\b(password|ssn|credit card|api key|token|personal data|salary|bank details)\b"


def extract_intent(goal_text, actor="user"):
    lowered = goal_text.lower()

    actions = re.findall(ACTION_WORDS, lowered)
    targets = re.findall(TARGET_WORDS, lowered)
    data_refs = re.findall(DATA_WORDS, lowered)

    risk_score = 5
    hits = []
    for kw, score in RISK_KEYWORDS.items():
        if kw in lowered:
            risk_score += score
            hits.append(kw)
    risk_score = min(risk_score, 100)

    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 35:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    fingerprint_src = f"{actor}|{sorted(set(actions))}|{sorted(set(targets))}|{sorted(set(data_refs))}"
    fingerprint = hashlib.sha256(fingerprint_src.encode()).hexdigest()[:32]

    return {
        "goal": goal_text,
        "actor": actor,
        "actions": sorted(set(actions)) or ["analyze"],
        "targets": sorted(set(targets)) or ["general"],
        "data_refs": sorted(set(data_refs)),
        "risk_keywords_hit": hits,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "intent_fingerprint": fingerprint,
        "drift_detected": False,
    }
