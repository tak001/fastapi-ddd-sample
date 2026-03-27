from application.chat.chat_service import ChatAgentPort, ChatResponse
from application.chat.send_message import SendMessageCommand, SendMessageUseCase


class StubChatAgent(ChatAgentPort):
    def process_message(self, session_id: str, user_message: str) -> ChatResponse:
        return ChatResponse(
            response=f"Received: {user_message}",
            created_goal_ids=[],
            created_task_ids=[],
        )


class TestSendMessageUseCase:
    def test_delegates_to_chat_agent(self) -> None:
        agent = StubChatAgent()
        use_case = SendMessageUseCase(agent)
        result = use_case.execute(SendMessageCommand(session_id="s1", message="Hello"))
        assert result.response == "Received: Hello"

    def test_passes_session_id_to_agent(self) -> None:
        calls: list[tuple[str, str]] = []

        class SpyChatAgent(ChatAgentPort):
            def process_message(self, session_id: str, user_message: str) -> ChatResponse:
                calls.append((session_id, user_message))
                return ChatResponse(response="ok", created_goal_ids=[], created_task_ids=[])

        use_case = SendMessageUseCase(SpyChatAgent())
        use_case.execute(SendMessageCommand(session_id="test-session", message="Hi"))
        assert calls == [("test-session", "Hi")]
