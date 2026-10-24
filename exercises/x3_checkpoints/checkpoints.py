from pydantic import BaseModel, Field
from typing import Annotated
from operator import add
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

# Pydantic State Schema
class State(BaseModel):
    nlist: Annotated[list[str], add] = Field(default_factory=list)

# Node Definitions
def node_a(state: State) -> State:
    print(f"Hello from Node A! Receiving: {state.nlist}")
    return State(nlist=["A"])

def node_b(state: State) -> State:
    print(f"Hello from Node B! Receiving: {state.nlist}")
    return State(nlist=["B"])

def node_c(state: State) -> State:
    print(f"Hello from Node C! Receiving: {state.nlist}")
    return State(nlist=["C"])

def invoke_graph(greeting: str) -> None:
    # StateGraph Builder
    builder = StateGraph(State, input_schema=State)

    # Add Nodes
    builder.add_node("node_a", node_a)
    builder.add_node("node_b", node_b)
    builder.add_node("node_c", node_c)

    # Add Edges
    builder.add_edge(START, "node_a")
    builder.add_edge(START, "node_b")
    builder.add_edge("node_a", "node_c")
    builder.add_edge("node_b", "node_c")
    builder.add_edge("node_c", END)

    # Define the Checkpointer
    checkpointer = InMemorySaver()

    # Compile Graph
    graph = builder.compile(checkpointer=checkpointer)

    # Define Graph Config
    initial_state = State(nlist = [greeting])
    config: RunnableConfig = {"configurable": {"thread_id": "1"}}

    # Invoke with Config
    graph.invoke(initial_state, config)

    # Print Graph State
    print(f"\nGraph State: {graph.get_state(config)}")

    # Generate Graph
    # Uncomment to draw the graph -> (graph.png)
    graph.get_graph().draw_mermaid_png(output_file_path="exercises/x3_checkpoints/graph.png")