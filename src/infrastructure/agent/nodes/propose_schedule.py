"""Node: Propose a schedule for the pending tasks."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

if TYPE_CHECKING:
    from langchain_anthropic import ChatAnthropic

SCHEDULE_SYSTEM_PROMPT = """You are a scheduling expert.
Given prioritized tasks, create a daily schedule proposal.
Format each day as: "YYYY-MM-DD: task title"
Group tasks by day and provide a brief rationale.
Keep the response concise and actionable.
Respond in the same language as the user's original message."""


def build_propose_schedule_node(llm: ChatAnthropic):  # type: ignore[type-arg]
    def propose_schedule(state: dict[str, Any]) -> dict[str, Any]:
        pending = state.get("pending_tasks", [])
        if not pending:
            return {"messages": [AIMessage(content="No tasks to schedule.")]}
        original_messages = state.get("messages", [])
        messages = [
            SystemMessage(content=SCHEDULE_SYSTEM_PROMPT),
            *original_messages[:1],
            HumanMessage(content=f"Tasks to schedule:\n{json.dumps(pending, ensure_ascii=False)}"),
        ]
        response = llm.invoke(messages)
        return {"messages": [AIMessage(content=str(response.content))]}

    return propose_schedule
