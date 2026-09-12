# Agentic AI Security Pipeline

A working demo of a 9-stage security pipeline for agentic AI systems — every
stage of an autonomous agent's reasoning loop is checked by a dedicated
security mechanism, with a tamper-evident hash-chain audit log running
across the whole flow.

## Pipeline stages

| # | Stage | Security Mechanism |
|---|-------|---------------------|
| 1 | User (Goal) | — |
| 2 | Intent Understanding | Intent DNA Fingerprint |
| 3 | Goal Contract / Intent Lock | Allow/deny policy engine |
| 4 | Planning (Task Breakdown) | Capability Budget Graph |
| 5 | Tool Selection | Action Shadow Simulation (sandboxed dry-run) |
| 6 | Execution (Actions) | Proof-Carrying Memory |
| 7 | Memory / Evaluation | Memory Trust Score + Failure DNA |
| 8 | Loop (Repeat) | Kill Switch (caps retries/cost/time) |
| 9 | Final Output | Outcome Proof Certificate |

Cross-cutting: **Hash Chain Logger** (SHA-256 tamper-evident audit trail,
`audit_log.jsonl`) and **AI Flow Trace** (end-to-end step + anomaly tracking).

## Quick start

### Option A — one command (Mac/Linux)
```bash
chmod +x run.sh
./run.sh
```

### Option B — one command (Windows)
```bat
run.bat
```

### Option C — manual
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:8000**

## Demo script for judges

1. Try the **low-risk preset** ("Search recent invoices...") → watch it sail
   through all 9 stages with a high confidence score.
2. Try the **high-risk preset** ("Delete the customer database and transfer
   funds...") → watch Stage 2 flag HIGH risk, Stage 3 partially block the
   goal contract, and Stage 7/8 trip the kill switch on repeated blocked
   actions.
3. Click **"View Audit Chain"** to show the SHA-256 hash-chained log of
   every stage.
4. Click **"Simulate Tamper Attack"** — this edits one log entry directly
   on disk without recomputing its hash. Click **"View Audit Chain"** again
   and watch the chain verification turn red and pinpoint the exact
   tampered entry — proving the hash chain actually detects tampering, not
   just displays a badge.
5. Click **"Reset Log"** to start a clean run for the next demo.

## Project structure

```
app.py                          FastAPI server + REST endpoints
core/
  pipeline.py                   Orchestrates all 9 stages
  hash_chain_logger.py          SHA-256 tamper-evident audit log
  flow_trace.py                 End-to-end step/anomaly tracking
security/
  intent_understanding.py       Stage 2 — Intent DNA Fingerprint
  goal_contract.py               Stage 3 — Goal Contract / Intent Lock
  capability_budget.py          Stage 4 — Capability Budget Graph
  action_shadow_sim.py          Stage 5 — Action Shadow Simulation
  proof_carrying_memory.py      Stage 6 — Proof-Carrying Memory
  memory_trust_score.py         Stage 6b — Memory Trust Score
  failure_dna.py                Stage 7 — Failure DNA + Kill Switch
  outcome_proof.py              Stage 9 — Outcome Proof Certificate
static/index.html               Dashboard UI (vanilla JS, no build step)
```

## Notes

- All tool execution is **simulated in a local sandbox** — no real external
  systems are touched. This is safe to run and demo anywhere.
- The risk scoring, budget limits, and kill-switch thresholds are simple,
  transparent, tunable rules — built to be explained live to judges, not a
  black box.
- `audit_log.jsonl` is created on first run and grows with every pipeline
  execution. Delete it (or click "Reset Log") to start fresh.
