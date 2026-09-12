"""
Pipeline orchestrator — wires all 9 stages together, each protected by its
own security mechanism, with Hash Chain Logger + AI Flow Trace running
across the whole flow.
"""
from security import intent_understanding as s2
from security import goal_contract as s3
from security import capability_budget as s4
from security import action_shadow_sim as s5
from security import proof_carrying_memory as s6
from security import memory_trust_score as s6b
from security import failure_dna as s7
from security import outcome_proof as s9

from core.hash_chain_logger import HashChainLogger
from core.flow_trace import FlowTrace


def run_pipeline(goal_text, actor="user", log_path="audit_log.jsonl", max_failures=3):
    logger = HashChainLogger(log_path)
    trace = FlowTrace()
    stages = {}

    # ---- Stage 1: User (Goal) ----
    stage1 = {"goal": goal_text, "actor": actor}
    logger.append("1_user_goal", stage1)
    trace.track("User (Goal)", "done", stage1)
    stages["1_user"] = stage1

    # ---- Stage 2: Intent Understanding -> Intent DNA Fingerprint ----
    intent = s2.extract_intent(goal_text, actor)
    logger.append("2_intent_understanding", intent)
    trace.track("Intent Understanding", "done", intent, anomaly=(intent["risk_level"] == "HIGH"))
    stages["2_intent"] = intent

    # ---- Stage 3: Planning lock -> Goal Contract / Intent Lock ----
    contract = s3.build_contract(intent)
    logger.append("3_goal_contract", contract)
    trace.track("Goal Contract / Intent Lock", "done", contract, anomaly=(not contract["enforced"]))
    stages["3_contract"] = contract

    # ---- Stage 4: Planning (Task Breakdown) -> Capability Budget Graph ----
    plan = s4.build_plan(intent, contract)
    logger.append("4_planning_budget", plan)
    trace.track("Planning (Capability Budget Graph)", "done", plan, anomaly=(not plan["within_budget"]))
    stages["4_plan"] = plan

    # ---- Stages 5-8 loop per subtask: Tool Selection -> Execution -> Memory -> Evaluation ----
    kill_switch = s7.KillSwitch(max_failures=max_failures)
    step_results = []
    for subtask in plan["subtasks"]:
        if kill_switch.tripped:
            trace.track(f"Loop step {subtask['step']}", "skipped_kill_switch", subtask, anomaly=True)
            break

        # Stage 5: Tool Selection -> Action Shadow Simulation
        sim = s5.simulate(subtask)
        logger.append(f"5_shadow_sim_step{subtask['step']}", sim)
        trace.track(f"Tool Selection / Shadow Sim (step {subtask['step']})", "done", sim,
                     anomaly=(sim["decision"] != "APPROVE"))

        # Stage 6: Execution -> Proof-Carrying Memory
        exec_res = s6.execute_action(subtask, sim)
        logger.append(f"6_execution_step{subtask['step']}", exec_res)
        trace.track(f"Execution (step {subtask['step']})",
                     "done" if exec_res["executed"] else "blocked", exec_res,
                     anomaly=(not exec_res["executed"]))

        # Memory Update -> Memory Trust Score
        mem = s6b.score_memory(exec_res)
        logger.append(f"6b_memory_step{subtask['step']}", mem)
        trace.track(f"Memory Update (step {subtask['step']})", "done", mem)

        # Stage 7 (Evaluation) -> Failure DNA + Kill Switch
        evaln = kill_switch.evaluate(sim, exec_res)
        logger.append(f"7_evaluation_step{subtask['step']}", evaln)
        trace.track(f"Evaluation (step {subtask['step']})", "done", evaln, anomaly=evaln["failed"])

        step_results.append({
            "subtask": subtask, "sim": sim, "exec": exec_res, "memory": mem, "eval": evaln,
        })

    stages["5_8_loop_steps"] = step_results

    # ---- Stage 9: Final Output -> Outcome Proof Certificate ----
    evaluations = [s["eval"] for s in step_results]
    certificate = s9.certify(intent, evaluations)
    logger.append("9_final_output", certificate)
    trace.track("Final Output (Outcome Proof Certificate)", "done", certificate)
    stages["9_certificate"] = certificate

    chain_ok, problems = logger.verify_chain()

    return {
        "stages": stages,
        "kill_switch_tripped": kill_switch.tripped,
        "audit_chain_valid": chain_ok,
        "audit_chain_problems": problems,
        "flow_trace": trace.to_list(),
    }
