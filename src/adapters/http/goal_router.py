from collections.abc import Callable

from fastapi import APIRouter, Depends, status

from adapters.http.schemas.goal_schemas import (
    CreateGoalRequest,
    GoalListResponse,
    GoalResponse,
)
from application.goal.create_goal import CreateGoalCommand, CreateGoalUseCase
from application.goal.get_goal import GetGoalQuery, GetGoalUseCase
from application.goal.list_goals import ListGoalsQuery, ListGoalsUseCase


def create_goal_router(
    get_create_use_case: Callable[[], CreateGoalUseCase],
    get_get_use_case: Callable[[], GetGoalUseCase],
    get_list_use_case: Callable[[], ListGoalsUseCase],
) -> APIRouter:
    router = APIRouter(prefix="/goals", tags=["goals"])

    @router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
    def create_goal(
        request: CreateGoalRequest,
        use_case: CreateGoalUseCase = Depends(get_create_use_case),
    ) -> GoalResponse:
        result = use_case.execute(
            CreateGoalCommand(title=request.title, description=request.description)
        )
        return GoalResponse(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
        )

    @router.get("", response_model=GoalListResponse)
    def list_goals(
        use_case: ListGoalsUseCase = Depends(get_list_use_case),
    ) -> GoalListResponse:
        result = use_case.execute(ListGoalsQuery())
        return GoalListResponse(
            goals=[
                GoalResponse(
                    id=g.id, title=g.title, description=g.description, status=g.status
                )
                for g in result.goals
            ]
        )

    @router.get("/{goal_id}", response_model=GoalResponse)
    def get_goal(
        goal_id: str,
        use_case: GetGoalUseCase = Depends(get_get_use_case),
    ) -> GoalResponse:
        result = use_case.execute(GetGoalQuery(goal_id=goal_id))
        return GoalResponse(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
            task_ids=result.task_ids,
        )

    return router
