"""Task definitions for PS01-PS05. Every tool is a lightweight mock -
enough to demonstrate the KAVACH checkpoints (risk scoring, scope
gating, PII redaction, tamper-evident logging) around a realistic
shape of agent action, without needing a real document store, ATS, or
database wired up for a hackathon prototype."""

import os
from .base import TaskDefinition

# ---------------------------------------------------------------- PS01
# Agentic Government Document Intelligence Assistant

def ps01_retrieve_sections(query: str = ""):
    return {"matches": [{"doc": "Circular_2024_17.pdf", "section": "3.2", "snippet": "..."}]}

def ps01_compare_documents(doc_a: str = "", doc_b: str = ""):
    return {"changes": ["clause 4 threshold raised", "clause 7 added"]}

def ps01_generate_summary(topic: str = ""):
    return {"summary": f"Structured summary of provisions related to '{topic}'."}

PS01 = TaskDefinition(
    ps_id="PS01", name="Government Document Intelligence Assistant",
    objective="Answer questions, compare, and summarize government circulars/orders with citations.",
    tool_registry={
        "retrieve_sections": ps01_retrieve_sections,
        "compare_documents": ps01_compare_documents,
        "generate_summary": ps01_generate_summary,
    },
    tool_docs={
        "retrieve_sections": "find relevant sections across ingested documents for a query",
        "compare_documents": "diff two documents and list what changed",
        "generate_summary": "produce a structured, cited summary on a topic",
    },
    tool_risk={"retrieve_sections": 0.1, "compare_documents": 0.2, "generate_summary": 0.2},
    default_scopes=["docs:query"],
    scope_gated_tools={"generate_summary": "docs:query"},
)

# ---------------------------------------------------------------- PS02
# AI-Powered Citizen Complaint Understanding & Resolution Assistant

def ps02_classify_complaint(category_hint: str = ""):
    return {"category": category_hint or "general", "confidence": 0.9}

def ps02_check_duplicate(area: str = "unspecified"):
    return {"is_duplicate": False}

def ps02_route_to_department(department: str = "general_helpdesk"):
    return {"routed_to": department, "ticket_id": "TCK-" + os.urandom(3).hex().upper()}

def ps02_notify_citizen(phone: str = "", message: str = ""):
    return {"sent_to": phone, "message": message}

PS02 = TaskDefinition(
    ps_id="PS02", name="Citizen Complaint Understanding & Resolution Assistant",
    objective="Convert a free-form citizen complaint into a categorized, routed, tracked service ticket.",
    tool_registry={
        "classify_complaint": ps02_classify_complaint,
        "check_duplicate": ps02_check_duplicate,
        "route_to_department": ps02_route_to_department,
        "notify_citizen": ps02_notify_citizen,
    },
    tool_docs={
        "classify_complaint": "detect complaint type from the text, e.g. category_hint",
        "check_duplicate": "check if a similar complaint already exists in this area",
        "route_to_department": "assign the ticket to a responsible department",
        "notify_citizen": "send a status SMS to the citizen's phone (needs consent)",
    },
    tool_risk={"classify_complaint": 0.1, "check_duplicate": 0.1, "route_to_department": 0.3, "notify_citizen": 0.5},
    default_scopes=["complaint:submit", "notify:sms"],
    scope_gated_tools={"notify_citizen": "notify:sms"},
)

# ---------------------------------------------------------------- PS03
# Multi-Agent Resume Screening & Job Matching Platform

def ps03_parse_resume(resume_id: str = ""):
    return {"skills": ["python", "sql"], "experience_years": 3}

def ps03_parse_job(job_id: str = ""):
    return {"required_skills": ["python", "aws"], "min_experience": 2}

def ps03_compute_match(resume_id: str = "", job_id: str = ""):
    return {"match_score": 0.78}

def ps03_skill_gap_report(resume_id: str = "", job_id: str = ""):
    return {"missing_skills": ["aws"]}

def ps03_rank_candidates(job_id: str = ""):
    return {"ranking": ["resume_12", "resume_04", "resume_09"]}

PS03 = TaskDefinition(
    ps_id="PS03", name="Resume Screening & Job Matching Platform",
    objective="Evaluate resumes against job descriptions and produce explainable, ranked matches.",
    tool_registry={
        "parse_resume": ps03_parse_resume, "parse_job": ps03_parse_job,
        "compute_match": ps03_compute_match, "skill_gap_report": ps03_skill_gap_report,
        "rank_candidates": ps03_rank_candidates,
    },
    tool_docs={
        "parse_resume": "extract skills/experience from a resume",
        "parse_job": "extract requirements from a job description",
        "compute_match": "score compatibility between a resume and a job",
        "skill_gap_report": "list skills the candidate is missing for a job",
        "rank_candidates": "produce a ranked candidate list for a job posting",
    },
    tool_risk={"parse_resume": 0.1, "parse_job": 0.1, "compute_match": 0.2, "skill_gap_report": 0.2, "rank_candidates": 0.3},
    default_scopes=["recruiting:screen"],
    scope_gated_tools={"rank_candidates": "recruiting:screen"},
)

# ---------------------------------------------------------------- PS04
# Agentic Research Paper Discovery & Literature Review Assistant

def ps04_search_papers(topic: str = ""):
    return {"papers": ["Smith et al. 2023", "Rao et al. 2024"]}

def ps04_summarize_paper(paper_id: str = ""):
    return {"summary": "Uses CNNs for early-stage detection on leaf imagery."}

def ps04_identify_methodology(paper_id: str = ""):
    return {"methodology": "supervised CNN classification", "dataset": "PlantVillage"}

def ps04_find_research_gaps(topic: str = ""):
    return {"gaps": ["limited field-condition data", "no multilingual farmer-facing UI"]}

PS04 = TaskDefinition(
    ps_id="PS04", name="Research Paper Discovery & Literature Review Assistant",
    objective="Conduct a structured literature review: find papers, summarize, extract methods, find gaps.",
    tool_registry={
        "search_papers": ps04_search_papers, "summarize_paper": ps04_summarize_paper,
        "identify_methodology": ps04_identify_methodology, "find_research_gaps": ps04_find_research_gaps,
    },
    tool_docs={
        "search_papers": "search for papers relevant to a topic",
        "summarize_paper": "summarize a specific paper",
        "identify_methodology": "extract methodology/dataset used by a paper",
        "find_research_gaps": "identify open research gaps on a topic",
    },
    tool_risk={"search_papers": 0.1, "summarize_paper": 0.2, "identify_methodology": 0.2, "find_research_gaps": 0.3},
    default_scopes=["research:query"],
    scope_gated_tools={},
)

# ---------------------------------------------------------------- PS05
# Autonomous Data Analyst Agent

def ps05_inspect_dataset(dataset: str = ""):
    return {"columns": ["district", "cases", "beds_available"], "rows": 640}

def ps05_clean_data(dataset: str = ""):
    return {"rows_dropped": 12, "nulls_filled": 34}

def ps05_compute_statistics(dataset: str = ""):
    return {"mean_cases": 214.5, "std_cases": 88.1}

def ps05_detect_anomalies(dataset: str = ""):
    return {"anomalous_districts": ["Sitapur", "Deoria"]}

def ps05_generate_report(dataset: str = ""):
    return {"report": "3 districts show statistically unusual healthcare load."}

PS05 = TaskDefinition(
    ps_id="PS05", name="Autonomous Data Analyst Agent",
    objective="Inspect, clean, analyze a dataset and explain findings to a non-technical user.",
    tool_registry={
        "inspect_dataset": ps05_inspect_dataset, "clean_data": ps05_clean_data,
        "compute_statistics": ps05_compute_statistics, "detect_anomalies": ps05_detect_anomalies,
        "generate_report": ps05_generate_report,
    },
    tool_docs={
        "inspect_dataset": "look at columns/row count of the uploaded dataset",
        "clean_data": "handle nulls/bad rows in the dataset",
        "compute_statistics": "compute summary statistics",
        "detect_anomalies": "flag unusual rows/groups in the data",
        "generate_report": "write a final plain-language findings report",
    },
    tool_risk={"inspect_dataset": 0.1, "clean_data": 0.3, "compute_statistics": 0.2, "detect_anomalies": 0.3, "generate_report": 0.2},
    default_scopes=["data:analyze"],
    scope_gated_tools={},
)

ALL = [PS01, PS02, PS03, PS04, PS05]
