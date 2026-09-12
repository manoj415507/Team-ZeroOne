"""
KAVACH backend (v2) - generic across all 20 problem statements.

One shared HashChainLogger, one shared secret, one TaskDefinition
registry (tasks/). Selecting a different ps_id changes only which
tools/risk-table/prompt are used - every request, for every PS, goes
through the exact same ConsentGate -> IntentFirewall -> PlanningBroker
-> ToolSandbox -> HashChainLogger sequence.

Run:
    cd kavach_sdk
    pip install -r requirements.txt -r backend/requirements.txt
    # put ANTHROPIC_API_KEY and KAVACH_SECRET in kavach_sdk/.env (see .env.example)
    uvicorn backend.main:app --reload --port 8000
"""

import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from kavach import KavachPipeline
from kavach.audit import HashChainLogger
from tasks import REGISTRY

load_dotenv()

CLAUDE_MODEL = "claude-sonnet-5"
SECRET = os.environ.get("KAVACH_SECRET", "dev-secret-change-me")
LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "unified_audit_log.jsonl")

# ONE logger, shared by every task's pipeline -> one chain of evidence
# across all 20 problem statements, not 20 disconnected log files.
shared_logger = HashChainLogger(LOG_PATH)

claude = Anthropic()

app = FastAPI(title="KAVACH API - unified pipeline for 20 problem statements")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # demo only
    allow_methods=["*"],
    allow_headers=["*"],
)

_pipeline_cache: dict[str, KavachPipeline] = {}


def get_pipeline(ps_id: str) -> KavachPipeline:
    if ps_id not in REGISTRY:
        raise HTTPException(status_code=404, detail=f"unknown ps_id '{ps_id}'")
    if ps_id not in _pipeline_cache:
        task = REGISTRY[ps_id]
        _pipeline_cache[ps_id] = KavachPipeline(
            secret_key=SECRET,
            tool_registry=task.tool_registry,
            extra_tool_risk=task.tool_risk,
            shared_logger=shared_logger,
        )
    return _pipeline_cache[ps_id]


# ---- request/response models -----------------------------------------

class SessionRequest(BaseModel):
    user_id: str
    ps_id: str

class RunRequest(BaseModel):
    session_token: str
    ps_id: str
    message: str


# ---- Claude: generic planner shared by all 20 tasks --------------------

def get_agent_decision(task, safe_text: str) -> dict:
    response = claude.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=500,
        system=task.planner_system_prompt(),
        messages=[{"role": "user", "content": safe_text}],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.strip("`").removeprefix("json").strip()
    return json.loads(raw)


# ---- routes -------------------------------------------------------------

@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {"ps_id": t.ps_id, "name": t.name, "objective": t.objective, "default_scopes": t.default_scopes}
            for t in REGISTRY.values()
        ]
    }


@app.post("/session")
def create_session(req: SessionRequest):
    task = REGISTRY.get(req.ps_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"unknown ps_id '{req.ps_id}'")
    pipeline = get_pipeline(req.ps_id)
    token = pipeline.issue_session(req.user_id, task.default_scopes)
    return {"session_token": token, "scopes": task.default_scopes, "ps_id": req.ps_id}


@app.post("/run")
def run_task(req: RunRequest):
    task = REGISTRY.get(req.ps_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"unknown ps_id '{req.ps_id}'")
    pipeline = get_pipeline(req.ps_id)

    # Stage 1 preview - decide what Claude is even allowed to see
    preview = pipeline.firewall.screen(req.message)
    if preview.blocked:
        return {
            "allowed": False,
            "reason": "blocked at intent firewall before reaching the agent",
            "injection_score": preview.injection_score,
        }

    try:
        decision = get_agent_decision(task, preview.safe_text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"agent planning failed: {exc}")

    proposed_plan = task.build_plan(decision)
    result = pipeline.handle_request(req.session_token, req.message, proposed_plan)

    return {
        "ps_id": req.ps_id,
        "task_name": task.name,
        "allowed": result.allowed,
        "reason": result.reason,
        "safe_text": result.safe_text,
        "injection_score": result.injection_score,
        "agent_decision": decision if result.allowed else None,
        "plan_summary": result.plan_summary,
        "tool_results": result.tool_results,
        "pending_human_approval": result.pending_human_approval,
    }


@app.get("/audit/log")
def get_audit_log(limit: int = 60):
    if not os.path.exists(LOG_PATH):
        return {"entries": []}
    with open(LOG_PATH) as f:
        lines = f.readlines()[-limit:]
    return {"entries": [json.loads(line) for line in lines]}


@app.get("/audit/verify")
def verify_audit_log():
    valid, broken_at = shared_logger.verify()
    return {"valid": valid, "broken_at_line": broken_at}


@app.post("/audit/simulate-tamper")
def simulate_tamper():
    """Demo-only: mutates one existing log line's payload without
    touching its stored hash, so /audit/verify catches it live."""
    if not os.path.exists(LOG_PATH):
        raise HTTPException(status_code=400, detail="no log entries yet - run a task first")
    with open(LOG_PATH) as f:
        lines = f.readlines()
    if not lines:
        raise HTTPException(status_code=400, detail="no log entries yet - run a task first")

    idx = len(lines) // 2
    entry = json.loads(lines[idx])
    if "user_id" in entry:
        entry["user_id"] = str(entry["user_id"]) + "_TAMPERED"
    elif "reason" in entry:
        entry["reason"] = "TAMPERED"
    else:
        entry["event"] = str(entry.get("event", "")) + "_TAMPERED"
    lines[idx] = json.dumps(entry, sort_keys=True) + "\n"
    with open(LOG_PATH, "w") as f:
        f.writelines(lines)
    return {"tampered_line": idx + 1}


@app.get("/health")
def health():
    return {"status": "ok", "tasks_loaded": len(REGISTRY)}
