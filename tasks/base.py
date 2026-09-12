"""
TaskDefinition - the single shape every problem statement (PS01-PS20)
is expressed in. Only the DATA differs per task (tools, their risk
levels, the consent scope they need, and a one-line objective for the
planner prompt) - the planner-prompt template and the plan-building
logic are written ONCE here and reused by all 20 tasks and by
KavachPipeline unchanged.

This is what makes "one security pipeline for every problem statement"
literally true in the code, not just a claim in the architecture doc:
every task is compiled through the exact same TaskDefinition.build_plan
and then executed through the exact same KavachPipeline.handle_request.
"""

from dataclasses import dataclass, field


@dataclass
class TaskDefinition:
    ps_id: str                     # "PS01".."PS20"
    name: str                      # short display name
    objective: str                 # one-line goal, used in the planner prompt
    tool_registry: dict            # tool_name -> callable(**args)
    tool_docs: dict                # tool_name -> one-line description for the planner
    tool_risk: dict                # tool_name -> risk float 0-1 (fed into extra_tool_risk)
    default_scopes: list[str] = field(default_factory=list)
    scope_gated_tools: dict = field(default_factory=dict)  # tool_name -> required_scope

    def planner_system_prompt(self) -> str:
        tool_lines = "\n".join(f"- {n}: {d}" for n, d in self.tool_docs.items())
        return f"""You are an autonomous agent for this task: {self.name}.
Objective: {self.objective}

You only ever receive PII-redacted text - tokens like <<PII:PHONE:1>> stand in
for real personal data. Never try to guess or reconstruct the real value.

Available tools (use ONLY these tool names, spelled exactly as given):
{tool_lines}

Decide which tools to call, in what order, and with what arguments, to handle
the user's request well. Respond with ONLY a JSON object, no other text, no
markdown fences:
{{"steps": [{{"tool": "<tool_name>", "args": {{...}}}}, ...]}}"""

    def build_plan(self, decision: dict) -> list[dict]:
        """Turn the LLM's proposed steps into the plan format KavachPipeline
        expects. Any tool the LLM names that isn't actually registered for
        this task is silently dropped here - and would be blocked by the
        planning broker's allow-list check anyway if it slipped through."""
        steps = []
        for raw in decision.get("steps", []):
            tool = raw.get("tool")
            if tool not in self.tool_registry:
                continue
            step = {"tool": tool, "args": raw.get("args", {}) or {}}
            if tool in self.scope_gated_tools:
                step["required_scope"] = self.scope_gated_tools[tool]
            steps.append(step)
        return steps
