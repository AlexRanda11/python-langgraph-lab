from pydantic import BaseModel, Field
from typing import Annotated
from langgraph.graph import START, END, StateGraph

# Reducer Function
def append_strings(left: list[str], right: list[str]) -> list[str]:
    """Combine the existing state value (left) with a node update (right)."""
    return left + right

# Pydantic State Schema
class State(BaseModel):
    nlist: Annotated[list[str], append_strings] = Field(default_factory=list)

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

    # Compile Graph
    graph = builder.compile()

    # Invoke with Greeting
    initial_state = State(nlist = [greeting])
    graph.invoke(initial_state)

    # Generate Graph
    # Uncomment to draw the graph -> (graph.png)
    graph.get_graph().draw_mermaid_png(output_file_path="examples/static_edges/graph.png")