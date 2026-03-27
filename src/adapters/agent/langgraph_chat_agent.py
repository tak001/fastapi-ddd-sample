"""LangGraph implementation of ChatAgentPort."""

from __future__ import annotations

from langchain_core.messages import HumanMessage
from langgraph.graph.state import CompiledStateGraph

from application.chat.chat_service import ChatAgentPort, ChatResponse


class LangGraphChatAgent(ChatAgentPort):
    def __init__(self, graph: CompiledStateGraph) -> None:
        self._graph = graph

    def process_message(self, session_id: str, user_message: str) -> ChatResponse:
        config = {"configurable": {"thread_id": session_id}}
        initial_state = {
            "messages": [HumanMessage(content=user_message)],
            "session_id": session_id,
            "intent": "",
            "pending_tasks": [],
            "created_goal_ids": [],
            "created_task_ids": [],
            "task_updates": [],
        }
        result = self._graph.invoke(initial_state, config)

        response_text = ""
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            response_text = str(last_msg.content) if hasattr(last_msg, "content") else ""

        return ChatResponse(
            response=response_text,
            created_goal_ids=tuple(result.get("created_goal_ids", [])),
            created_task_ids=tuple(result.get("created_task_ids", [])),
        )
