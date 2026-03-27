"""Node: Prioritize and reorder pending tasks."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

if TYPE_CHECKING:
    from langchain_anthropic import ChatAnthropic

PRIORITIZE_SYSTEM_PROMPT = """You are a task prioritization expert.
Given a list of tasks, reorder them by priority and adjust priorities if needed.
Consider dependencies between tasks and urgency.

Respond ONLY with the reordered JSON array of tasks (same format as input)."""


def build_prioritize_node(llm: ChatAnthropic):  # type: ignore[type-arg]
    def prioritize(state: dict[str, Any]) -> dict[str, Any]:
        pending = state.get("pending_tasks", [])
        if not pending:
            return {}
        messages = [
            SystemMessage(content=PRIORITIZE_SYSTEM_PROMPT),
            HumanMessage(content=json.dumps(pending, ensure_ascii=False)),
        ]
        response = llm.invoke(messages)
        content = str(response.content).strip()
        try:
            prioritized = json.loads(content)
            if not isinstance(prioritized, list):
                prioritized = pending
        except json.JSONDecodeError:
            prioritized = pending
        return {
            "pending_tasks": prioritized,
            "messages": [AIMessage(content="Tasks have been prioritized.")],
        }

    return prioritize
