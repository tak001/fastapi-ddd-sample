from dataclasses import dataclass

from application.chat.chat_service import ChatAgentPort, ChatResponse
from application.shared.use_case import UseCase


@dataclass(frozen=True)
class SendMessageCommand:
    session_id: str
    message: str


class SendMessageUseCase(UseCase[SendMessageCommand, ChatResponse]):
    def __init__(self, chat_agent: ChatAgentPort) -> None:
        self._chat_agent = chat_agent

    def execute(self, input_data: SendMessageCommand) -> ChatResponse:
        return self._chat_agent.process_message(
            session_id=input_data.session_id,
            user_message=input_data.message,
        )
