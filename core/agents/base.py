import os

from langchain_openai import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

from typing import Annotated, Callable, Optional, Any
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class AbstractAgent:
    def __init__(self, tools: list, verbose: bool = True):
        self.tools = tools
        self.verbose = verbose
        self.llm = self._get_llm()
        self.graph = self._build_graph()
        self.tools_map = {tool.name: tool for tool in tools}
        self.stream_callback = None

    def _get_llm(self):
        if os.getenv("OPENAI_API_KEY"):
            return ChatOpenAI(
                temperature=0,
                model="gpt-3.5-turbo",
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        else:
            llm = ChatOllama(model="llama3.1:latest",
                             verbose=self.verbose, temperature=0.0, num_predict=5000)
            llm_with_tools = llm.bind_tools(self.tools)
            return llm_with_tools

    def _build_graph(self):
        graph_builder = StateGraph(AgentState)

        def agent_node(state: AgentState, stream_callback: Optional[Callable[[dict], Any]] = None):
            msg = self.llm.invoke(state["messages"])

            tool_calls = getattr(msg, "tool_calls", [])

            filtered_tool_calls = []
            seen_tool_names = set()
            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                if tool_name and tool_name in self.tools_map and tool_name not in seen_tool_names:
                    filtered_tool_calls.append(tool_call)
                    seen_tool_names.add(tool_name)

            if stream_callback and filtered_tool_calls:
                stream_callback({
                    "type": "tool_calls",
                    "tool_calls": filtered_tool_calls,
                })

            processed_tools = []
            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                if tool_name is not None and tool_name not in processed_tools and tool_name in self.tools_map:
                    tool = self.tools_map[tool_name]
                else:
                    continue
                processed_tools.append(tool_name)

                tool_response = tool.invoke(tool_call)
                state["messages"].append(tool_response)

                if stream_callback:
                    stream_callback({
                        "type": "tool_response",
                        "tool_name": tool_name,
                        "tool_response": str(tool_response),
                    })

            ai_msg = self.llm.invoke(state["messages"])
            if not ai_msg.content:
                ai_msg = AIMessage(
                    content="I don't understand, can you please rephrase the question?")

            state["messages"].append(ai_msg)

            if stream_callback:
                stream_callback({
                    "type": "agent_response",
                    "content": ai_msg.content,
                })
            return {"messages": state["messages"]}

        def agent_node_with_callback(state: AgentState):
            return agent_node(state, stream_callback=self.stream_callback)

        graph_builder.add_node("agent", agent_node_with_callback)
        graph_builder.set_entry_point("agent")
        return graph_builder.compile()

    def run(self, system_prompt: str, user_prompt: str, stream_callback: Optional[Callable[[dict], Any]] = None) -> str:
        self.stream_callback = stream_callback

        initial_state = {
            "messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        }

        if stream_callback:
            stream_callback({"type": "user_prompt", "content": user_prompt, })

        result = self.graph.invoke(initial_state)

        print(result)
        return result["messages"][-1].content
