from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from adapters.http.chat_router import create_chat_router
from adapters.http.goal_router import create_goal_router
from adapters.http.task_router import create_task_router
from domain.goal.exceptions import GoalNotFoundError, GoalValidationError
from domain.task.exceptions import TaskNotFoundError, TaskValidationError
from infrastructure.config.di import (
    get_create_goal_use_case,
    get_create_task_use_case,
    get_get_goal_use_case,
    get_get_task_use_case,
    get_list_goals_use_case,
    get_list_tasks_use_case,
    get_send_message_use_case,
)

app = FastAPI(title="Task API", version="0.1.0")

app.include_router(
    create_task_router(get_create_task_use_case, get_get_task_use_case, get_list_tasks_use_case)
)
app.include_router(
    create_goal_router(get_create_goal_use_case, get_get_goal_use_case, get_list_goals_use_case)
)
app.include_router(create_chat_router(get_send_message_use_case))


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(TaskNotFoundError)
def handle_task_not_found(_request: Request, exc: TaskNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(TaskValidationError)
def handle_task_validation(_request: Request, exc: TaskValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(GoalNotFoundError)
def handle_goal_not_found(_request: Request, exc: GoalNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(GoalValidationError)
def handle_goal_validation(_request: Request, exc: GoalValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})
