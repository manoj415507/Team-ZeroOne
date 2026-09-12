"""Task definitions for PS16-PS20."""

import os
from .base import TaskDefinition

# ---------------------------------------------------------------- PS16
# Autonomous Scheme-Bundle Optimizer for Citizens

def ps16_fetch_eligible_schemes(profile: str = ""):
    return {"eligible": ["PM-Kisan", "Ayushman Bharat", "Ujjwala Yojana"]}

def ps16_detect_conflicts(schemes: str = ""):
    return {"conflicts": [("SchemeA", "SchemeB", "mutually exclusive income bracket")]}

def ps16_optimize_bundle(profile: str = ""):
    return {"recommended_bundle": ["PM-Kisan", "Ayushman Bharat"]}

def ps16_generate_checklist(bundle: str = ""):
    return {"documents_needed": ["Aadhaar", "land record", "income certificate"]}

PS16 = TaskDefinition(
    ps_id="PS16", name="Scheme-Bundle Optimizer for Citizens",
    objective="Find eligible government schemes for a citizen, resolve conflicts, and optimize the best bundle.",
    tool_registry={
        "fetch_eligible_schemes": ps16_fetch_eligible_schemes, "detect_conflicts": ps16_detect_conflicts,
        "optimize_bundle": ps16_optimize_bundle, "generate_checklist": ps16_generate_checklist,
    },
    tool_docs={
        "fetch_eligible_schemes": "find schemes a citizen profile is potentially eligible for",
        "detect_conflicts": "detect schemes that can't be combined",
        "optimize_bundle": "pick the best compatible combination of schemes",
        "generate_checklist": "list documents needed to apply for the chosen bundle",
    },
    tool_risk={"fetch_eligible_schemes": 0.1, "detect_conflicts": 0.2, "optimize_bundle": 0.3, "generate_checklist": 0.2},
    default_scopes=["citizen:benefits"],
    scope_gated_tools={},
)

# ---------------------------------------------------------------- PS17
# Multi-Agent Municipal Complaint Router with SLA Escalation

def ps17_classify_complaint(category_hint: str = ""):
    return {"category": category_hint or "general"}

def ps17_route_department(category: str = ""):
    return {"department": "sanitation" if "garbage" in category else "public_works"}

def ps17_set_priority(category: str = ""):
    return {"priority": "high" if "water" in category else "normal"}

def ps17_check_sla(ticket_id: str = ""):
    return {"sla_hours_remaining": 6}

def ps17_escalate_overdue(ticket_id: str = ""):
    return {"escalated": True}

PS17 = TaskDefinition(
    ps_id="PS17", name="Municipal Complaint Router with SLA Escalation",
    objective="Classify and route municipal complaints, then monitor and escalate SLA breaches.",
    tool_registry={
        "classify_complaint": ps17_classify_complaint, "route_department": ps17_route_department,
        "set_priority": ps17_set_priority, "check_sla": ps17_check_sla, "escalate_overdue": ps17_escalate_overdue,
    },
    tool_docs={
        "classify_complaint": "detect complaint category (garbage, water, road, streetlight, ...)",
        "route_department": "route the ticket to the responsible department",
        "set_priority": "assign an SLA priority to the ticket",
        "check_sla": "check how much SLA time remains on a ticket",
        "escalate_overdue": "escalate a ticket that has breached its SLA",
    },
    tool_risk={"classify_complaint": 0.1, "route_department": 0.2, "set_priority": 0.2, "check_sla": 0.1, "escalate_overdue": 0.5},
    default_scopes=["municipal:complaint"],
    scope_gated_tools={"escalate_overdue": "municipal:complaint"},
)

# ---------------------------------------------------------------- PS18
# Agentic Freelance Contract Risk Reviewer

def ps18_parse_contract(contract_id: str = ""):
    return {"clauses_found": 14}

def ps18_identify_clauses(contract_id: str = ""):
    return {"flagged_clauses": ["unlimited liability", "no kill-fee on termination"]}

def ps18_assess_risk(clause: str = ""):
    return {"severity": "high"}

def ps18_generate_plain_explanation(clause: str = ""):
    return {"explanation": "This clause makes you liable for damages with no upper limit."}

def ps18_suggest_revision(clause: str = ""):
    return {"suggested_text": "Liability shall not exceed the total fees paid under this agreement."}

PS18 = TaskDefinition(
    ps_id="PS18", name="Freelance Contract Risk Reviewer",
    objective="Review a freelance contract, flag risky clauses, explain them plainly, and suggest revisions.",
    tool_registry={
        "parse_contract": ps18_parse_contract, "identify_clauses": ps18_identify_clauses,
        "assess_risk": ps18_assess_risk, "generate_plain_explanation": ps18_generate_plain_explanation,
        "suggest_revision": ps18_suggest_revision,
    },
    tool_docs={
        "parse_contract": "parse an uploaded contract into clauses",
        "identify_clauses": "flag potentially unfair or risky clauses",
        "assess_risk": "assign a severity level to a flagged clause",
        "generate_plain_explanation": "explain a clause's impact in plain language",
        "suggest_revision": "propose fairer replacement wording for a clause",
    },
    tool_risk={"parse_contract": 0.2, "identify_clauses": 0.2, "assess_risk": 0.3, "generate_plain_explanation": 0.2, "suggest_revision": 0.3},
    default_scopes=["contract:review"],
    scope_gated_tools={},
)

# ---------------------------------------------------------------- PS19
# Agentic Career Pivot Advisor with Market/Skill/Finance Sub-Agents

def ps19_analyze_market(target_career: str = ""):
    return {"demand": "growing", "median_salary": 1200000}

def ps19_assess_skill_gap(current_role: str = "", target_career: str = ""):
    return {"missing_skills": ["cloud architecture", "system design"]}

def ps19_plan_finances(months_runway_needed: int = 6):
    return {"recommended_savings_buffer_months": months_runway_needed}

def ps19_generate_roadmap(target_career: str = ""):
    return {"roadmap": ["3mo upskilling", "portfolio project", "targeted applications"]}

PS19 = TaskDefinition(
    ps_id="PS19", name="Career Pivot Advisor",
    objective="Combine market demand, skill-gap, and financial-runway analysis into a career-transition roadmap.",
    tool_registry={
        "analyze_market": ps19_analyze_market, "assess_skill_gap": ps19_assess_skill_gap,
        "plan_finances": ps19_plan_finances, "generate_roadmap": ps19_generate_roadmap,
    },
    tool_docs={
        "analyze_market": "assess demand and pay for a target career",
        "assess_skill_gap": "compare current skills against the target role's requirements",
        "plan_finances": "estimate the savings runway needed for the transition",
        "generate_roadmap": "produce a timeline covering upskilling, portfolio, and job search",
    },
    tool_risk={"analyze_market": 0.1, "assess_skill_gap": 0.1, "plan_finances": 0.2, "generate_roadmap": 0.2},
    default_scopes=["career:advise"],
    scope_gated_tools={},
)

# ---------------------------------------------------------------- PS20
# Agentic Disaster Relief & Emergency Resource Coordinator

def ps20_ingest_zone_report(zone: str = "", severity: str = "medium"):
    return {"zone": zone, "severity": severity, "logged": True}

def ps20_assess_needs(zone: str = ""):
    return {"needs": {"food_kits": 500, "medical_teams": 2}}

def ps20_allocate_resources(zone: str = "", food_kits: int = 0, medical_teams: int = 0):
    return {"allocated_to": zone, "food_kits": food_kits, "medical_teams": medical_teams}

def ps20_detect_duplicate_effort(zone: str = ""):
    return {"duplicate_agencies_present": False}

def ps20_coordinate_agencies(zone: str = ""):
    return {"agencies_notified": ["NDRF", "local_ngo_1"]}

PS20 = TaskDefinition(
    ps_id="PS20", name="Disaster Relief & Emergency Resource Coordinator",
    objective="Ingest zone reports, assess needs, allocate/re-allocate relief resources, and coordinate agencies.",
    tool_registry={
        "ingest_zone_report": ps20_ingest_zone_report, "assess_needs": ps20_assess_needs,
        "allocate_resources": ps20_allocate_resources, "detect_duplicate_effort": ps20_detect_duplicate_effort,
        "coordinate_agencies": ps20_coordinate_agencies,
    },
    tool_docs={
        "ingest_zone_report": "log an incoming report from an affected zone",
        "assess_needs": "estimate resource needs for a zone",
        "allocate_resources": "commit resources (food, medical teams) to a zone",
        "detect_duplicate_effort": "check whether another agency is already covering this zone",
        "coordinate_agencies": "notify the agencies responding to a zone",
    },
    tool_risk={"ingest_zone_report": 0.2, "assess_needs": 0.2, "allocate_resources": 0.6, "detect_duplicate_effort": 0.2, "coordinate_agencies": 0.4},
    default_scopes=["disaster:coordinate"],
    scope_gated_tools={"allocate_resources": "disaster:coordinate"},
)

ALL = [PS16, PS17, PS18, PS19, PS20]
