"""Node: Parse task update intent to extract task_id and new status."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from langchain_core.messages import HumanMessage, SystemMessage

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel

PARSE_UPDATE_PROMPT = """You are a task update parser for a task management system.
Extract the task ID and new status from the user's message.

Valid statuses: "todo", "in_progress", "done"

Respond ONLY with a JSON array of updates. Each item must have:
- "task_id": the task ID string
- "status": the new status ("todo", "in_progress", or "done")

If you cannot identify a specific task ID, respond with an empty array: []
Example: [{"task_id": "abc123", "status": "done"}]"""


def build_parse_task_update_node(llm: "BaseChatModel") -> Any:
    def parse_task_update(state: dict[str, Any]) -> dict[str, Any]:
        messages = [SystemMessage(content=PARSE_UPDATE_PROMPT), *state["messages"][-3:]]
        response = llm.invoke(messages)
        content = str(response.content).strip()
        try:
            updates = json.loads(content)
            if not isinstance(updates, list):
                updates = []
        except json.JSONDecodeError:
            updates = []
        return {"task_updates": updates}

    return parse_task_update
