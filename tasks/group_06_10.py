"""Task definitions for PS06-PS10."""

import os
from .base import TaskDefinition

# ---------------------------------------------------------------- PS06
# Autonomous SQL Database Analyst

def ps06_generate_sql(question: str = ""):
    return {"sql": "SELECT district, SUM(unemployment_increase) FROM stats GROUP BY district ORDER BY 2 DESC LIMIT 5"}

def ps06_execute_query(sql: str = ""):
    return {"rows": [{"district": "Barmer", "value": 4.2}, {"district": "Kota", "value": 3.9}]}

def ps06_validate_result(sql: str = ""):
    return {"row_count_sane": True, "no_full_table_scan_without_limit": True}

def ps06_visualize_result():
    return {"chart": "bar_chart_top5_districts.png"}

PS06 = TaskDefinition(
    ps_id="PS06", name="Autonomous SQL Database Analyst",
    objective="Turn a natural-language question into SQL, run it, validate, visualize, and explain the result.",
    tool_registry={
        "generate_sql": ps06_generate_sql, "execute_query": ps06_execute_query,
        "validate_result": ps06_validate_result, "visualize_result": ps06_visualize_result,
    },
    tool_docs={
        "generate_sql": "translate a natural-language question into SQL",
        "execute_query": "run a validated SQL query against the database (read-only)",
        "validate_result": "sanity-check a query/result before trusting it",
        "visualize_result": "chart the query result",
    },
    tool_risk={"generate_sql": 0.2, "execute_query": 0.6, "validate_result": 0.1, "visualize_result": 0.2},
    default_scopes=["db:query"],
    scope_gated_tools={"execute_query": "db:query"},
)

# ---------------------------------------------------------------- PS07
# AI-Based Fake News & Claim Verification System

def ps07_extract_claims(text: str = ""):
    return {"claims": ["The bridge was built in 1990."]}

def ps07_retrieve_evidence(claim: str = ""):
    return {"sources": ["gov-infra-records.example", "news-archive.example"]}

def ps07_classify_claim(claim: str = ""):
    return {"verdict": "contradicted", "confidence": 0.81}

def ps07_rank_sources(claim: str = ""):
    return {"ranked": ["gov-infra-records.example", "news-archive.example"]}

def ps07_generate_report(claim: str = ""):
    return {"report": "Claim contradicted by government infrastructure records (built 1987)."}

PS07 = TaskDefinition(
    ps_id="PS07", name="Fake News & Claim Verification System",
    objective="Extract factual claims, retrieve evidence, and classify claims with a cited explanation.",
    tool_registry={
        "extract_claims": ps07_extract_claims, "retrieve_evidence": ps07_retrieve_evidence,
        "classify_claim": ps07_classify_claim, "rank_sources": ps07_rank_sources,
        "generate_report": ps07_generate_report,
    },
    tool_docs={
        "extract_claims": "pull out checkable factual claims from a text",
        "retrieve_evidence": "find sources relevant to a claim",
        "classify_claim": "classify a claim as supported / contradicted / unverified",
        "rank_sources": "rank evidence sources by reliability",
        "generate_report": "write the final verdict report with citations",
    },
    tool_risk={"extract_claims": 0.1, "retrieve_evidence": 0.2, "classify_claim": 0.3, "rank_sources": 0.2, "generate_report": 0.2},
    default_scopes=["factcheck:submit"],
    scope_gated_tools={},
)

# ---------------------------------------------------------------- PS08
# Multi-Agent Cross-Department File Movement Tracker

def ps08_create_file_record(subject: str = ""):
    return {"file_id": "GOV-" + os.urandom(3).hex().upper(), "subject": subject}

def ps08_update_status(file_id: str = "", department: str = ""):
    return {"file_id": file_id, "current_department": department, "status": "pending"}

def ps08_send_reminder(file_id: str = "", officer: str = ""):
    return {"reminder_sent_to": officer}

def ps08_escalate_delay(file_id: str = "", days_overdue: int = 0):
    return {"escalated": True, "escalated_to": "department_head"}

PS08 = TaskDefinition(
    ps_id="PS08", name="Cross-Department File Movement Tracker",
    objective="Track a government file across departments, remind on delay, escalate SLA breaches.",
    tool_registry={
        "create_file_record": ps08_create_file_record, "update_status": ps08_update_status,
        "send_reminder": ps08_send_reminder, "escalate_delay": ps08_escalate_delay,
    },
    tool_docs={
        "create_file_record": "register a new file/workflow",
        "update_status": "move the file to a department and update its status",
        "send_reminder": "send an automated reminder to the responsible officer",
        "escalate_delay": "escalate an overdue file past its SLA",
    },
    tool_risk={"create_file_record": 0.2, "update_status": 0.3, "send_reminder": 0.3, "escalate_delay": 0.6},
    default_scopes=["govfile:manage"],
    scope_gated_tools={"escalate_delay": "govfile:manage"},
)

# ---------------------------------------------------------------- PS09
# Agentic Guardian for Real-Time Payment Scam Interception

KNOWN_RECIPIENTS = {"9876500000": "Landlord - Mr. Verma (verified)"}

def ps09_verify_recipient(account_or_phone: str = ""):
    known = KNOWN_RECIPIENTS.get(account_or_phone)
    return {"known_recipient": known is not None, "label": known or "unverified / new recipient"}

def ps09_check_risk_signals(urgency_language: bool = False, new_recipient: bool = False, amount: float = 0.0):
    score = 0.0
    reasons = []
    if urgency_language: score += 0.4; reasons.append("urgency/social-engineering language")
    if new_recipient: score += 0.3; reasons.append("recipient not previously verified")
    if amount > 20000: score += 0.3; reasons.append("high transaction amount")
    return {"risk_score": round(min(score, 1.0), 2), "reasons": reasons}

def ps09_process_payment(amount: float = 0.0, recipient: str = ""):
    return {"status": "processed", "amount": amount, "recipient": recipient, "txn_id": "TXN-" + os.urandom(3).hex().upper()}

def ps09_flag_for_review(reason: str = ""):
    return {"status": "held_for_review", "reason": reason}

PS09 = TaskDefinition(
    ps_id="PS09", name="Real-Time Payment Scam Interception Guardian",
    objective="Analyze a payment request for scam risk before it completes; verify, score, and gate high-risk transfers.",
    tool_registry={
        "verify_recipient": ps09_verify_recipient, "check_risk_signals": ps09_check_risk_signals,
        "process_payment": ps09_process_payment, "flag_for_review": ps09_flag_for_review,
    },
    tool_docs={
        "verify_recipient": "check whether the payment recipient is previously verified",
        "check_risk_signals": "score urgency language / new recipient / amount as fraud risk signals",
        "process_payment": "actually move the money (always needs final confirmation)",
        "flag_for_review": "hold the transaction for manual review instead of processing",
    },
    tool_risk={"verify_recipient": 0.1, "check_risk_signals": 0.1, "process_payment": 0.9, "flag_for_review": 0.2},
    default_scopes=["payment:initiate"],
    scope_gated_tools={"process_payment": "payment:initiate"},
)

# ---------------------------------------------------------------- PS10
# Agent for End-to-End RTI Drafting & Deadline Tracking

def ps10_draft_rti(request_text: str = ""):
    return {"draft": f"Formal RTI application drafted regarding: {request_text}"}

def ps10_preview_application(draft_id: str = ""):
    return {"preview_ready": True}

def ps10_track_deadline(application_id: str = ""):
    return {"due_date": "2026-10-12", "days_remaining": 30}

def ps10_generate_followup(application_id: str = ""):
    return {"followup_draft": "First follow-up letter drafted citing statutory deadline."}

PS10 = TaskDefinition(
    ps_id="PS10", name="RTI Drafting & Deadline Tracking Agent",
    objective="Guide a citizen from an information request through RTI drafting, submission, and deadline tracking.",
    tool_registry={
        "draft_rti": ps10_draft_rti, "preview_application": ps10_preview_application,
        "track_deadline": ps10_track_deadline, "generate_followup": ps10_generate_followup,
    },
    tool_docs={
        "draft_rti": "draft a formal RTI application from the citizen's request",
        "preview_application": "prepare a structured preview for the citizen to approve",
        "track_deadline": "track the statutory response deadline for a filed application",
        "generate_followup": "draft a follow-up/escalation once overdue",
    },
    tool_risk={"draft_rti": 0.2, "preview_application": 0.1, "track_deadline": 0.1, "generate_followup": 0.3},
    default_scopes=["rti:draft"],
    scope_gated_tools={},
)

ALL = [PS06, PS07, PS08, PS09, PS10]
