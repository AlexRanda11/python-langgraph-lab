from pydantic import BaseModel, Field
from typing import Annotated, Literal
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

def node_x(state: State) -> State:
    print(f"Hello from Node X! Receiving: {state.nlist}")
    return State(nlist=["X"])

# Conditional Routing Function
def routing_function(state: State) -> Literal["node_x", "__end__"]:
    select = state.nlist[-1]
    if select == "C":
        return "node_x"
    else:
        return "__end__"

def invoke_graph(greeting: str) -> None:
    # StateGraph Builder
    builder = StateGraph(State, input_schema=State)

    # Add Nodes
    builder.add_node("node_a", node_a)
    builder.add_node("node_b", node_b)
    builder.add_node("node_c", node_c)
    builder.add_node("node_x", node_x)

    # Add Edges
    builder.add_edge(START, "node_a")
    builder.add_edge(START, "node_b")
    builder.add_edge("node_a", "node_c")
    builder.add_edge("node_b", "node_c")

    # Add Conditional Edges
    builder.add_conditional_edges("node_c", routing_function)
    builder.add_edge("node_x", END)

    # Compile Graph
    graph = builder.compile()

    # Invoke with Greeting
    initial_state = State(nlist = [greeting])
    graph.invoke(initial_state)

    # Generate Diagram
    # Uncomment to draw the graph -> (graph.png)
    graph.get_graph().draw_mermaid_png(output_file_path="exercises/x2_conditional_edges/graph.png")