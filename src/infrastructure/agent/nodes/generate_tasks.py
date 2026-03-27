"""Node: Generate tasks from a goal using LLM."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from langchain_core.messages import AIMessage, SystemMessage

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel

GENERATE_SYSTEM_PROMPT = """You are a task planning expert.
Given the user's goal, break it down into 3-7 concrete, actionable daily tasks.

Respond with a JSON array of tasks. Each task should have:
- "title": short task title (max 100 chars)
- "description": brief description of what to do
- "priority": "high", "medium", or "low"
- "due_date": suggested due date in YYYY-MM-DD format

Respond ONLY with the JSON array, no other text."""


def build_generate_tasks_node(llm: "BaseChatModel"):  # type: ignore[type-arg]
    def generate_tasks(state: dict[str, Any]) -> dict[str, Any]:
        messages = [SystemMessage(content=GENERATE_SYSTEM_PROMPT), *state["messages"]]
        response = llm.invoke(messages)
        content = str(response.content).strip()
        try:
            tasks = json.loads(content)
            if not isinstance(tasks, list):
                tasks = []
        except json.JSONDecodeError:
            tasks = []

        if not tasks:
            return {
                "pending_tasks": [],
                "messages": [AIMessage(content="Sorry, I could not generate tasks for your goal. Please try rephrasing it.")],
            }

        return {
            "pending_tasks": tasks,
            "messages": [AIMessage(content=f"Generated {len(tasks)} tasks for your goal.")],
        }

    return generate_tasks
