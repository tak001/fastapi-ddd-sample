from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.task.exceptions import TaskNotFoundError, TaskValidationError
from infrastructure.http.task_router import router as task_router

app = FastAPI(title="Task API", version="0.1.0")

app.include_router(task_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(TaskNotFoundError)
def handle_task_not_found(_request: Request, exc: TaskNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(TaskValidationError)
def handle_task_validation(_request: Request, exc: TaskValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})
