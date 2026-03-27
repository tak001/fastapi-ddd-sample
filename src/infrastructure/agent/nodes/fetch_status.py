"""Node: Fetch current goal/task status and inject into messages."""

from __future__ import annotations

import json
from typing import Any

from langchain_core.messages import SystemMessage

from application.goal.list_goals import ListGoalsQuery, ListGoalsUseCase
from application.task.list_tasks_by_goal import ListTasksByGoalQuery, ListTasksByGoalUseCase


def build_fetch_status_node(
    list_goals_use_case: ListGoalsUseCase,
    list_tasks_by_goal_use_case: ListTasksByGoalUseCase,
) -> Any:
    def fetch_status(state: dict[str, Any]) -> dict[str, Any]:
        goals_result = list_goals_use_case.execute(ListGoalsQuery())
        status_data: list[dict[str, Any]] = []

        for goal in goals_result.goals:
            tasks_result = list_tasks_by_goal_use_case.execute(
                ListTasksByGoalQuery(goal_id=goal.id)
            )
            status_data.append(
                {
                    "goal_id": goal.id,
                    "goal_title": goal.title,
                    "goal_status": goal.status,
                    "tasks": [
                        {
                            "task_id": t.id,
                            "title": t.title,
                            "status": t.status,
                            "priority": t.priority,
                            "due_date": t.due_date,
                        }
                        for t in tasks_result.tasks
                    ],
                }
            )

        summary = json.dumps(status_data, ensure_ascii=False)
        return {
            "messages": [SystemMessage(content=f"Current goals and tasks:\n{summary}")]
        }

    return fetch_status
