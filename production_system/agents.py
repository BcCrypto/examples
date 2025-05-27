from langgraph.graph import StateGraph
from autogen import AssistantAgent, UserProxyAgent
from pydantic import BaseModel


class TradingState(BaseModel):
    signal: str
    decision: str


def build_lang_app():
    graph = StateGraph(TradingState)
    graph.add_node("detect_signal", lambda state: state.copy(update={"signal": "buy"}))
    graph.add_node(
        "make_decision",
        lambda state: state.copy(update={"decision": f"Act on {state.signal}"}),
    )
    graph.set_entry_point("detect_signal")
    graph.add_edge("detect_signal", "make_decision")
    graph.set_finish_point("make_decision")
    return graph.compile()


def create_agents():
    signal_agent = AssistantAgent(name="Signal Analyzer", llm_config={"temperature": 0})
    decision_agent = AssistantAgent(name="Trade Decider", llm_config={"temperature": 0})
    user_agent = UserProxyAgent(name="Controller", code_execution_config={"work_dir": "."})
    return signal_agent, decision_agent, user_agent
