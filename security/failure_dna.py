"""
Stage 7 (Evaluation) — Failure DNA + Kill Switch
Classifies failures, detects repeated failure patterns, and trips a kill
switch after too many consecutive failures to cap retries/time/cost.
"""


class KillSwitch:
    def __init__(self, max_failures=3):
        self.max_failures = max_failures
        self.consecutive_failures = 0
        self.failure_signatures = set()
        self.tripped = False

    def evaluate(self, sim_result, exec_result):
        failed = sim_result["decision"] != "APPROVE" or not exec_result.get("executed")

        repeated = False
        if failed:
            self.consecutive_failures += 1
            signature = f"{sim_result['action']}:{sim_result['decision']}"
            repeated = signature in self.failure_signatures
            self.failure_signatures.add(signature)
        else:
            self.consecutive_failures = 0

        if self.consecutive_failures >= self.max_failures:
            self.tripped = True

        return {
            "step": sim_result["step"],
            "failed": failed,
            "failure_type": sim_result["decision"] if failed else None,
            "repeated_pattern": repeated,
            "consecutive_failures": self.consecutive_failures,
            "kill_switch_tripped": self.tripped,
            "action_taken": "ROLLBACK+ESCALATE" if self.tripped else ("RETRY_ALLOWED" if failed else "CONTINUE"),
        }
