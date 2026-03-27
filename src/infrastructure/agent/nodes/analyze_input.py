"""Node: Analyze user input to classify intent."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from langchain_core.messages import SystemMessage

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel

ANALYZE_SYSTEM_PROMPT = """You are an intent classifier for a goal/task management system.
Classify the user's latest message into exactly one of these intents:
- "create_goal": User wants to set a new goal or objective
- "check_status": User wants to see their goals or tasks
- "update_task": User wants to update a task's status
- "general_chat": Other conversation

Respond with ONLY the intent string, nothing else."""


def build_analyze_input_node(llm: "BaseChatModel"):  # type: ignore[type-arg]
    def analyze_input(state: dict[str, Any]) -> dict[str, Any]:
        messages = [SystemMessage(content=ANALYZE_SYSTEM_PROMPT), *state["messages"][-5:]]
        response = llm.invoke(messages)
        content = str(response.content).strip().strip('"').lower()
        valid_intents = {"create_goal", "check_status", "update_task", "general_chat"}
        intent = content if content in valid_intents else "general_chat"
        return {"intent": intent}

    return analyze_input
