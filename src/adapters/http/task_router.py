from collections.abc import Callable

from fastapi import APIRouter, Depends, status

from adapters.http.schemas.task_schemas import (
    CreateTaskRequest,
    TaskListResponse,
    TaskResponse,
)
from application.task.create_task import CreateTaskCommand, CreateTaskUseCase
from application.task.get_task import GetTaskQuery, GetTaskUseCase
from application.task.list_tasks import ListTasksQuery, ListTasksUseCase


def create_task_router(
    get_create_use_case: Callable[[], CreateTaskUseCase],
    get_get_use_case: Callable[[], GetTaskUseCase],
    get_list_use_case: Callable[[], ListTasksUseCase],
) -> APIRouter:
    router = APIRouter(prefix="/tasks", tags=["tasks"])

    @router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
    def create_task(
        request: CreateTaskRequest,
        use_case: CreateTaskUseCase = Depends(get_create_use_case),
    ) -> TaskResponse:
        result = use_case.execute(
            CreateTaskCommand(
                title=request.title,
                description=request.description,
                goal_id=request.goal_id,
                priority=request.priority,
                due_date=request.due_date,
            )
        )
        return TaskResponse(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
            priority=result.priority,
            goal_id=result.goal_id,
            due_date=result.due_date,
        )

    @router.get("", response_model=TaskListResponse)
    def list_tasks(
        use_case: ListTasksUseCase = Depends(get_list_use_case),
    ) -> TaskListResponse:
        result = use_case.execute(ListTasksQuery())
        return TaskListResponse(
            tasks=[
                TaskResponse(
                    id=item.id,
                    title=item.title,
                    description=item.description,
                    status=item.status,
                    priority=item.priority,
                    goal_id=item.goal_id,
                    due_date=item.due_date,
                )
                for item in result.tasks
            ]
        )

    @router.get("/{task_id}", response_model=TaskResponse)
    def get_task(
        task_id: str,
        use_case: GetTaskUseCase = Depends(get_get_use_case),
    ) -> TaskResponse:
        result = use_case.execute(GetTaskQuery(task_id=task_id))
        return TaskResponse(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
            priority=result.priority,
            goal_id=result.goal_id,
            due_date=result.due_date,
        )

    return router
