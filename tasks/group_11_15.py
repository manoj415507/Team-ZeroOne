"""Task definitions for PS11-PS15."""

from .base import TaskDefinition

# ---------------------------------------------------------------- PS11
# Agentic Vendor Negotiator for Routine Government Procurement

def ps11_request_quotation(vendor: str = ""):
    return {"vendor": vendor, "quote": 48500}

def ps11_compare_quotations(vendors: str = ""):
    return {"lowest": "vendor_b", "amount": 46200}

def ps11_negotiate_terms(vendor: str = "", target_price: float = 0.0):
    return {"counter_offer": target_price * 0.95, "vendor_response": "pending"}

def ps11_approve_within_limit(amount: float = 0.0):
    return {"approved": amount <= 50000}

PS11 = TaskDefinition(
    ps_id="PS11", name="Vendor Negotiator for Routine Procurement",
    objective="Communicate with vendors, compare quotations, and negotiate within predefined policy limits.",
    tool_registry={
        "request_quotation": ps11_request_quotation, "compare_quotations": ps11_compare_quotations,
        "negotiate_terms": ps11_negotiate_terms, "approve_within_limit": ps11_approve_within_limit,
    },
    tool_docs={
        "request_quotation": "ask a vendor for a quotation",
        "compare_quotations": "compare quotations across vendors",
        "negotiate_terms": "propose a counter-offer to a vendor within policy",
        "approve_within_limit": "approve a procurement amount if within the configured limit",
    },
    tool_risk={"request_quotation": 0.2, "compare_quotations": 0.1, "negotiate_terms": 0.5, "approve_within_limit": 0.4},
    default_scopes=["procurement:negotiate"],
    scope_gated_tools={"negotiate_terms": "procurement:negotiate", "approve_within_limit": "procurement:negotiate"},
)

# ---------------------------------------------------------------- PS12
# Agentic Tutor Orchestrating Subject-Specialist Sub-Agents

def ps12_route_to_specialist(subject: str = ""):
    return {"routed_to": f"{subject}_specialist_agent"}

def ps12_update_progress(student_id: str = "", topic: str = ""):
    return {"progress_updated": True, "topic": topic}

def ps12_generate_recommendation(student_id: str = ""):
    return {"recommendation": "Review quadratic equations before moving to calculus."}

def ps12_fetch_student_context(student_id: str = ""):
    return {"recent_topics": ["algebra", "trigonometry"], "weak_areas": ["quadratics"]}

PS12 = TaskDefinition(
    ps_id="PS12", name="Agentic Tutor with Subject-Specialist Sub-Agents",
    objective="Route a student's question to the right subject specialist while maintaining a shared learning profile.",
    tool_registry={
        "route_to_specialist": ps12_route_to_specialist, "update_progress": ps12_update_progress,
        "generate_recommendation": ps12_generate_recommendation, "fetch_student_context": ps12_fetch_student_context,
    },
    tool_docs={
        "route_to_specialist": "hand the question off to a subject-specific specialist agent",
        "update_progress": "record what the student just learned/practiced",
        "generate_recommendation": "suggest the student's next best topic to study",
        "fetch_student_context": "load the student's recent topics and weak areas",
    },
    tool_risk={"route_to_specialist": 0.1, "update_progress": 0.1, "generate_recommendation": 0.2, "fetch_student_context": 0.2},
    default_scopes=["tutor:session"],
    scope_gated_tools={},
)

# ---------------------------------------------------------------- PS13
# Agentic Compliance Co-Pilot for Cross-Border E-Commerce Sellers

def ps13_analyze_listing(product: str = "", destination: str = ""):
    return {"product": product, "destination": destination}

def ps13_check_destination_rules(destination: str = ""):
    return {"restricted_categories": ["lithium batteries over 100Wh"], "labeling_required": ["CE mark"]}

def ps13_classify_risk(product: str = "", destination: str = ""):
    return {"risk": "medium", "issue": "battery capacity not declared"}

def ps13_generate_report(product: str = "", destination: str = ""):
    return {"report": "Add CE mark and declare battery Wh before listing."}

PS13 = TaskDefinition(
    ps_id="PS13", name="Cross-Border E-Commerce Compliance Co-Pilot",
    objective="Review a product listing against a destination market's compliance requirements.",
    tool_registry={
        "analyze_listing": ps13_analyze_listing, "check_destination_rules": ps13_check_destination_rules,
        "classify_risk": ps13_classify_risk, "generate_report": ps13_generate_report,
    },
    tool_docs={
        "analyze_listing": "read the product listing details",
        "check_destination_rules": "look up compliance rules for the destination country",
        "classify_risk": "classify the listing's compliance risk level",
        "generate_report": "produce a compliance report with remediation steps",
    },
    tool_risk={"analyze_listing": 0.1, "check_destination_rules": 0.1, "classify_risk": 0.3, "generate_report": 0.2},
    default_scopes=["compliance:review"],
    scope_gated_tools={},
)

# ---------------------------------------------------------------- PS14
# Autonomous Water-Sharing Dispute Mediation Agent for Farmers

def ps14_model_water_availability(canal: str = ""):
    return {"available_liters_per_day": 120000}

def ps14_detect_conflict(canal: str = ""):
    return {"conflict": True, "farmers_involved": ["farmer_a", "farmer_b"]}

def ps14_propose_schedule(canal: str = ""):
    return {"schedule": {"farmer_a": "Mon/Wed/Fri 6-9am", "farmer_b": "Tue/Thu/Sat 6-9am"}}

def ps14_record_agreement(canal: str = ""):
    return {"agreement_recorded": True}

PS14 = TaskDefinition(
    ps_id="PS14", name="Water-Sharing Dispute Mediation Agent",
    objective="Detect irrigation conflicts and propose a fair water-sharing schedule between farmers.",
    tool_registry={
        "model_water_availability": ps14_model_water_availability, "detect_conflict": ps14_detect_conflict,
        "propose_schedule": ps14_propose_schedule, "record_agreement": ps14_record_agreement,
    },
    tool_docs={
        "model_water_availability": "estimate available water for a canal/zone",
        "detect_conflict": "detect a scheduling conflict between farmers sharing a resource",
        "propose_schedule": "propose an allocation schedule to resolve the conflict",
        "record_agreement": "record the final agreed schedule",
    },
    tool_risk={"model_water_availability": 0.1, "detect_conflict": 0.2, "propose_schedule": 0.55, "record_agreement": 0.3},
    default_scopes=["mediation:propose"],
    scope_gated_tools={"propose_schedule": "mediation:propose"},
)

# ---------------------------------------------------------------- PS15
# Multi-Agent Fact-Verification Pipeline for Local Newsrooms

def ps15_decompose_article(article_id: str = ""):
    return {"claims": ["Local unemployment fell 2% this quarter."]}

def ps15_retrieve_evidence_15(claim: str = ""):
    return {"sources": ["state-labour-bureau.example"]}

def ps15_verify_claim(claim: str = ""):
    return {"verdict": "unverified", "confidence": 0.4}

def ps15_flag_conflicting_evidence(claim: str = ""):
    return {"conflict_found": True, "detail": "bureau report shows 0.4% rise, not a 2% fall"}

def ps15_generate_verification_report(article_id: str = ""):
    return {"report": "1 of 3 claims contradicted by primary source data."}

PS15 = TaskDefinition(
    ps_id="PS15", name="Fact-Verification Pipeline for Local Newsrooms",
    objective="Decompose an article into claims, verify each against evidence, and produce a verification report.",
    tool_registry={
        "decompose_article": ps15_decompose_article, "retrieve_evidence": ps15_retrieve_evidence_15,
        "verify_claim": ps15_verify_claim, "flag_conflicting_evidence": ps15_flag_conflicting_evidence,
        "generate_verification_report": ps15_generate_verification_report,
    },
    tool_docs={
        "decompose_article": "break an article into individually checkable claims",
        "retrieve_evidence": "find sources relevant to a specific claim",
        "verify_claim": "verify a single claim against retrieved evidence",
        "flag_conflicting_evidence": "flag when evidence contradicts the article",
        "generate_verification_report": "compile the final per-claim verification report",
    },
    tool_risk={"decompose_article": 0.1, "retrieve_evidence": 0.2, "verify_claim": 0.3, "flag_conflicting_evidence": 0.3, "generate_verification_report": 0.2},
    default_scopes=["newsroom:verify"],
    scope_gated_tools={},
)

ALL = [PS11, PS12, PS13, PS14, PS15]
