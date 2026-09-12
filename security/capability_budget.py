"""
Stage 4 — Planning (Task Breakdown)
Security Mechanism: Capability Budget Graph
"""


def build_plan(intent, contract):
    actions = contract["allowed_actions"] or ["analyze"]
    subtasks = []
    for i, a in enumerate(actions, 1):
        subtasks.append({
            "step": i,
            "action": a,
            "target": intent["targets"][0] if intent["targets"] else "general",
            "permission_budget": {
                "read": True,
                "write": a in ["create", "update", "install", "share"],
                "cost_usd": 0.5,
            },
        })

    total_cost = round(sum(s["permission_budget"]["cost_usd"] for s in subtasks), 2)
    within_budget = total_cost <= contract["limits"]["max_cost_usd"]

    max_steps_allowed = int(contract["limits"]["max_cost_usd"] / 0.5)
    blocked_out_of_scope = [] if within_budget else subtasks[max_steps_allowed:]
    if not within_budget:
        subtasks = subtasks[:max_steps_allowed]

    return {
        "subtasks": subtasks,
        "total_estimated_cost": total_cost,
        "budget_limit": contract["limits"]["max_cost_usd"],
        "within_budget": within_budget,
        "blocked_out_of_scope": blocked_out_of_scope,
    }
