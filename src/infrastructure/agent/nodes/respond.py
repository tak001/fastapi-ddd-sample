"""Node: Generate final response to user."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from langchain_core.messages import AIMessage, SystemMessage

if TYPE_CHECKING:
    from langchain_anthropic import ChatAnthropic

RESPOND_SYSTEM_PROMPT = """You are a helpful goal/task management assistant.
Based on the conversation, provide a clear and helpful response to the user.
If goals and tasks were created, summarize what was done.
If the user asked about status, provide a clear overview.
Always respond in the same language as the user's message.
Be concise and actionable."""


def build_respond_node(llm: ChatAnthropic):  # type: ignore[type-arg]
    def respond(state: dict[str, Any]) -> dict[str, Any]:
        messages = [SystemMessage(content=RESPOND_SYSTEM_PROMPT), *state["messages"]]
        response = llm.invoke(messages)
        return {"messages": [AIMessage(content=str(response.content))]}

    return respond
