"""StateGraph construction for goal/task management agent."""

from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from application.goal.add_task_to_goal import AddTaskToGoalUseCase
from application.goal.create_goal import CreateGoalUseCase
from application.goal.list_goals import ListGoalsUseCase
from application.task.create_task import CreateTaskUseCase
from application.task.list_tasks_by_goal import ListTasksByGoalUseCase
from application.task.update_task_status import UpdateTaskStatusUseCase
from infrastructure.agent.nodes.analyze_input import build_analyze_input_node
from infrastructure.agent.nodes.execute_tools import build_execute_tools_node
from infrastructure.agent.nodes.fetch_status import build_fetch_status_node
from infrastructure.agent.nodes.generate_tasks import build_generate_tasks_node
from infrastructure.agent.nodes.parse_task_update import build_parse_task_update_node
from infrastructure.agent.nodes.prioritize import build_prioritize_node
from infrastructure.agent.nodes.propose_schedule import build_propose_schedule_node
from infrastructure.agent.nodes.respond import build_respond_node
from infrastructure.agent.state import AgentState


def _route_by_intent(state: dict) -> str:
    intent = state.get("intent", "general_chat")
    if intent == "create_goal":
        return "generate_tasks"
    if intent == "check_status":
        return "fetch_status"
    if intent == "update_task":
        return "parse_task_update"
    return "respond"


def build_graph(
    llm: BaseChatModel,
    create_goal_use_case: CreateGoalUseCase,
    create_task_use_case: CreateTaskUseCase,
    add_task_to_goal_use_case: AddTaskToGoalUseCase,
    list_goals_use_case: ListGoalsUseCase,
    list_tasks_by_goal_use_case: ListTasksByGoalUseCase,
    update_task_status_use_case: UpdateTaskStatusUseCase,
    checkpointer: MemorySaver | None = None,
) -> CompiledStateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("analyze_input", build_analyze_input_node(llm))
    graph.add_node("generate_tasks", build_generate_tasks_node(llm))
    graph.add_node("prioritize", build_prioritize_node(llm))
    graph.add_node("propose_schedule", build_propose_schedule_node(llm))
    graph.add_node(
        "execute_tools",
        build_execute_tools_node(
            create_goal_use_case,
            create_task_use_case,
            add_task_to_goal_use_case,
            update_task_status_use_case,
        ),
    )
    graph.add_node(
        "fetch_status",
        build_fetch_status_node(list_goals_use_case, list_tasks_by_goal_use_case),
    )
    graph.add_node("parse_task_update", build_parse_task_update_node(llm))
    graph.add_node("respond", build_respond_node(llm))

    graph.add_edge(START, "analyze_input")
    graph.add_conditional_edges("analyze_input", _route_by_intent)
    graph.add_edge("generate_tasks", "prioritize")
    graph.add_edge("prioritize", "propose_schedule")
    graph.add_edge("propose_schedule", "execute_tools")
    graph.add_edge("execute_tools", "respond")
    graph.add_edge("fetch_status", "respond")
    graph.add_edge("parse_task_update", "execute_tools")
    graph.add_edge("respond", END)

    return graph.compile(checkpointer=checkpointer or MemorySaver())
