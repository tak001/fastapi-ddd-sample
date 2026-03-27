"""Composition Root: wires all dependencies together."""

import os

from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver

from application.chat.send_message import SendMessageUseCase
from application.goal.add_task_to_goal import AddTaskToGoalUseCase
from application.goal.create_goal import CreateGoalUseCase
from application.goal.get_goal import GetGoalUseCase
from application.goal.list_goals import ListGoalsUseCase
from application.task.create_task import CreateTaskUseCase
from application.task.get_task import GetTaskUseCase
from application.task.list_tasks import ListTasksUseCase
from application.task.list_tasks_by_goal import ListTasksByGoalUseCase
from application.task.update_task_status import UpdateTaskStatusUseCase
from infrastructure.agent.graph import build_graph
from adapters.agent.langgraph_chat_agent import LangGraphChatAgent
from infrastructure.persistence.in_memory_goal_repository import InMemoryGoalRepository
from infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository

_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not _api_key:
    raise RuntimeError(
        "ANTHROPIC_API_KEY is not set. "
        "Please set it in your environment or .env file."
    )

_llm_model = os.environ.get("LLM_MODEL", "claude-sonnet-4-20250514")

# Repositories
_task_repository = InMemoryTaskRepository()
_goal_repository = InMemoryGoalRepository()

# Task use cases
_create_task_use_case = CreateTaskUseCase(_task_repository)
_get_task_use_case = GetTaskUseCase(_task_repository)
_list_tasks_use_case = ListTasksUseCase(_task_repository)
_list_tasks_by_goal_use_case = ListTasksByGoalUseCase(_task_repository)
_update_task_status_use_case = UpdateTaskStatusUseCase(_task_repository)

# Goal use cases
_create_goal_use_case = CreateGoalUseCase(_goal_repository)
_get_goal_use_case = GetGoalUseCase(_goal_repository)
_list_goals_use_case = ListGoalsUseCase(_goal_repository)
_add_task_to_goal_use_case = AddTaskToGoalUseCase(_goal_repository)

# LangGraph agent
_llm = ChatAnthropic(model=_llm_model, api_key=_api_key)
_checkpointer = MemorySaver()
_compiled_graph = build_graph(
    llm=_llm,
    create_goal_use_case=_create_goal_use_case,
    create_task_use_case=_create_task_use_case,
    add_task_to_goal_use_case=_add_task_to_goal_use_case,
    list_goals_use_case=_list_goals_use_case,
    list_tasks_by_goal_use_case=_list_tasks_by_goal_use_case,
    update_task_status_use_case=_update_task_status_use_case,
    checkpointer=_checkpointer,
)
_chat_agent = LangGraphChatAgent(_compiled_graph)
_send_message_use_case = SendMessageUseCase(_chat_agent)


# Getter functions for FastAPI Depends()
def get_create_task_use_case() -> CreateTaskUseCase:
    return _create_task_use_case


def get_get_task_use_case() -> GetTaskUseCase:
    return _get_task_use_case


def get_list_tasks_use_case() -> ListTasksUseCase:
    return _list_tasks_use_case


def get_list_tasks_by_goal_use_case() -> ListTasksByGoalUseCase:
    return _list_tasks_by_goal_use_case


def get_update_task_status_use_case() -> UpdateTaskStatusUseCase:
    return _update_task_status_use_case


def get_create_goal_use_case() -> CreateGoalUseCase:
    return _create_goal_use_case


def get_get_goal_use_case() -> GetGoalUseCase:
    return _get_goal_use_case


def get_list_goals_use_case() -> ListGoalsUseCase:
    return _list_goals_use_case


def get_send_message_use_case() -> SendMessageUseCase:
    return _send_message_use_case
