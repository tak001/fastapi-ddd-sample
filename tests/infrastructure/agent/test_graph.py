"""Integration tests for the LangGraph agent graph.

These tests use a mock LLM to verify graph compilation and node routing
without making actual API calls.
"""

from __future__ import annotations

from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from application.goal.add_task_to_goal import AddTaskToGoalUseCase
from application.goal.create_goal import CreateGoalUseCase
from application.goal.list_goals import ListGoalsUseCase
from application.task.create_task import CreateTaskUseCase
from application.task.list_tasks_by_goal import ListTasksByGoalUseCase
from application.task.update_task_status import UpdateTaskStatusUseCase
from infrastructure.agent.graph import build_graph
from infrastructure.persistence.in_memory_goal_repository import InMemoryGoalRepository
from infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository


class FakeLLM:
    """Minimal fake LLM that returns predictable responses."""

    def __init__(self, responses: list[str] | None = None) -> None:
        self._responses = list(responses or ["general_chat"])
        self._call_count = 0

    def invoke(self, messages: list[BaseMessage], **kwargs: Any) -> AIMessage:
        idx = min(self._call_count, len(self._responses) - 1)
        content = self._responses[idx]
        self._call_count += 1
        return AIMessage(content=content)


def _build_graph(fake_llm: FakeLLM) -> Any:
    task_repo = InMemoryTaskRepository()
    goal_repo = InMemoryGoalRepository()
    return (
        build_graph(
            llm=fake_llm,  # type: ignore[arg-type]
            create_goal_use_case=CreateGoalUseCase(goal_repo),
            create_task_use_case=CreateTaskUseCase(task_repo),
            add_task_to_goal_use_case=AddTaskToGoalUseCase(goal_repo),
            list_goals_use_case=ListGoalsUseCase(goal_repo),
            list_tasks_by_goal_use_case=ListTasksByGoalUseCase(task_repo),
            update_task_status_use_case=UpdateTaskStatusUseCase(task_repo),
            checkpointer=MemorySaver(),
        ),
        task_repo,
        goal_repo,
    )


def _initial_state(content: str = "Hello") -> dict:
    return {
        "messages": [HumanMessage(content=content)],
        "session_id": "test",
        "intent": "",
        "pending_tasks": [],
        "created_goal_ids": [],
        "created_task_ids": [],
        "task_updates": [],
    }


class TestGraphCompilation:
    def test_graph_compiles_successfully(self) -> None:
        graph, _, _ = _build_graph(FakeLLM())
        assert graph is not None

    def test_general_chat_intent_routes_to_respond(self) -> None:
        graph, _, _ = _build_graph(FakeLLM(responses=["general_chat", "Hello! How can I help?"]))

        result = graph.invoke(_initial_state("Hello"), {"configurable": {"thread_id": "test-1"}})

        assert result["intent"] == "general_chat"
        assert len(result["messages"]) >= 2

    def test_create_goal_intent_generates_tasks(self) -> None:
        task_json = '[{"title":"Task 1","description":"Do it","priority":"high","due_date":"2026-04-01"}]'
        fake_llm = FakeLLM(
            responses=[
                "create_goal",
                task_json,
                task_json,
                "Here is your schedule",
                "Goal and tasks created!",
            ]
        )
        graph, task_repo, goal_repo = _build_graph(fake_llm)

        result = graph.invoke(
            _initial_state("Build a portfolio site"),
            {"configurable": {"thread_id": "test-2"}},
        )

        assert result["intent"] == "create_goal"
        assert len(result["created_goal_ids"]) == 1
        assert len(result["created_task_ids"]) >= 1
        assert len(goal_repo.find_all()) == 1
        assert len(task_repo.find_all()) >= 1

    def test_check_status_intent_routes_to_fetch_status(self) -> None:
        fake_llm = FakeLLM(responses=["check_status", "You have no goals yet."])
        graph, _, _ = _build_graph(fake_llm)

        result = graph.invoke(
            _initial_state("What are my goals?"),
            {"configurable": {"thread_id": "test-3"}},
        )

        assert result["intent"] == "check_status"
        assert len(result["messages"]) >= 2

    def test_generate_tasks_json_failure_returns_error_message(self) -> None:
        fake_llm = FakeLLM(
            responses=[
                "create_goal",
                "not valid json",
                "not valid json",
                "Sorry, I could not generate tasks for your goal. Please try rephrasing it.",
            ]
        )
        graph, task_repo, goal_repo = _build_graph(fake_llm)

        result = graph.invoke(
            _initial_state("Some goal"),
            {"configurable": {"thread_id": "test-4"}},
        )

        assert result["intent"] == "create_goal"
        assert len(goal_repo.find_all()) == 0
        assert len(task_repo.find_all()) == 0
