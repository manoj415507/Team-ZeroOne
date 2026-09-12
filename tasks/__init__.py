"""
tasks.REGISTRY - the single lookup table of all 20 problem statements.

Every entry is a TaskDefinition (see base.py): objective, tools, tool
risk, and consent scopes. The backend and CLI runner both go through
this registry so adding a 21st task later means adding ONE
TaskDefinition, not touching any pipeline/security code.
"""

from .base import TaskDefinition
from . import group_01_05, group_06_10, group_11_15, group_16_20

REGISTRY: dict[str, TaskDefinition] = {
    t.ps_id: t
    for t in (group_01_05.ALL + group_06_10.ALL + group_11_15.ALL + group_16_20.ALL)
}

__all__ = ["REGISTRY", "TaskDefinition"]
