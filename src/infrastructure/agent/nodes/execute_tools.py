"""Node: Execute tool calls to persist goals and tasks via use cases."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

from application.goal.add_task_to_goal import AddTaskToGoalCommand, AddTaskToGoalUseCase
from application.goal.create_goal import CreateGoalCommand, CreateGoalUseCase
from application.task.create_task import CreateTaskCommand, CreateTaskUseCase
from application.task.update_task_status import UpdateTaskStatusCommand, UpdateTaskStatusUseCase


def build_execute_tools_node(
    create_goal_use_case: CreateGoalUseCase,
    create_task_use_case: CreateTaskUseCase,
    add_task_to_goal_use_case: AddTaskToGoalUseCase,
    update_task_status_use_case: UpdateTaskStatusUseCase,
) -> Any:
    def execute_tools(state: dict[str, Any]) -> dict[str, Any]:
        intent = state.get("intent", "")

        if intent == "create_goal":
            return _handle_create_goal(
                state, create_goal_use_case, create_task_use_case, add_task_to_goal_use_case
            )
        if intent == "update_task":
            return _handle_update_task(state, update_task_status_use_case)
        return {}

    return execute_tools


def _handle_create_goal(
    state: dict[str, Any],
    create_goal_use_case: CreateGoalUseCase,
    create_task_use_case: CreateTaskUseCase,
    add_task_to_goal_use_case: AddTaskToGoalUseCase,
) -> dict[str, Any]:
    pending = state.get("pending_tasks", [])
    if not pending:
        return {}

    created_goal_ids: list[str] = list(state.get("created_goal_ids", []))
    created_task_ids: list[str] = list(state.get("created_task_ids", []))

    user_message = next(
        (str(msg.content) for msg in state.get("messages", []) if hasattr(msg, "type") and msg.type == "human"),
        "",
    )

    goal_result = create_goal_use_case.execute(
        CreateGoalCommand(title=user_message[:200], description=user_message)
    )
    goal_id = goal_result.id
    created_goal_ids.append(goal_id)

    for task_data in pending:
        task_result = create_task_use_case.execute(
            CreateTaskCommand(
                title=str(task_data.get("title", "Untitled"))[:100],
                description=str(task_data.get("description", "")),
                goal_id=goal_id,
                priority=str(task_data.get("priority", "medium")),
                due_date=task_data.get("due_date"),
            )
        )
        created_task_ids.append(task_result.id)
        add_task_to_goal_use_case.execute(
            AddTaskToGoalCommand(goal_id=goal_id, task_id=task_result.id)
        )

    return {
        "created_goal_ids": created_goal_ids,
        "created_task_ids": created_task_ids,
    }


def _handle_update_task(
    state: dict[str, Any],
    update_task_status_use_case: UpdateTaskStatusUseCase,
) -> dict[str, Any]:
    task_updates: list[dict[str, str]] = state.get("task_updates", [])

    for update in task_updates:
        task_id = update.get("task_id", "")
        new_status = update.get("status", "")
        if not task_id or not new_status:
            continue
        try:
            update_task_status_use_case.execute(
                UpdateTaskStatusCommand(task_id=task_id, new_status=new_status)
            )
        except Exception as e:
            logger.warning("Failed to update task %s to status %s: %s", task_id, new_status, e)

    return {}
