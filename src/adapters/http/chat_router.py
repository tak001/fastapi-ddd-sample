import asyncio
from collections.abc import Callable

from fastapi import APIRouter, Depends

from adapters.http.schemas.chat_schemas import ChatRequest, ChatResponseSchema
from application.chat.send_message import SendMessageCommand, SendMessageUseCase


def create_chat_router(
    get_send_message_use_case: Callable[[], SendMessageUseCase],
) -> APIRouter:
    router = APIRouter(prefix="/chat", tags=["chat"])

    @router.post("", response_model=ChatResponseSchema)
    async def chat(
        request: ChatRequest,
        use_case: SendMessageUseCase = Depends(get_send_message_use_case),
    ) -> ChatResponseSchema:
        result = await asyncio.to_thread(
            use_case.execute,
            SendMessageCommand(session_id=request.session_id, message=request.message),
        )
        return ChatResponseSchema(
            response=result.response,
            created_goal_ids=list(result.created_goal_ids),
            created_task_ids=list(result.created_task_ids),
        )

    return router
