from fastapi import APIRouter, Depends, status

from application.task.create_task import CreateTaskCommand, CreateTaskUseCase
from application.task.get_task import GetTaskQuery, GetTaskUseCase
from application.task.list_tasks import ListTasksQuery, ListTasksUseCase
from infrastructure.config.di import (
    get_create_task_use_case,
    get_get_task_use_case,
    get_list_tasks_use_case,
)
from infrastructure.http.schemas.task_schemas import (
    CreateTaskRequest,
    TaskListResponse,
    TaskResponse,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    request: CreateTaskRequest,
    use_case: CreateTaskUseCase = Depends(get_create_task_use_case),
) -> TaskResponse:
    result = use_case.execute(
        CreateTaskCommand(title=request.title, description=request.description)
    )
    return TaskResponse(
        id=result.id,
        title=result.title,
        description=result.description,
        status=result.status,
    )


@router.get("", response_model=TaskListResponse)
def list_tasks(
    use_case: ListTasksUseCase = Depends(get_list_tasks_use_case),
) -> TaskListResponse:
    result = use_case.execute(ListTasksQuery())
    return TaskListResponse(
        tasks=[
            TaskResponse(
                id=item.id,
                title=item.title,
                description=item.description,
                status=item.status,
            )
            for item in result.tasks
        ]
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    use_case: GetTaskUseCase = Depends(get_get_task_use_case),
) -> TaskResponse:
    result = use_case.execute(GetTaskQuery(task_id=task_id))
    return TaskResponse(
        id=result.id,
        title=result.title,
        description=result.description,
        status=result.status,
    )
