from pydantic import BaseModel, Field
from typing import Annotated
from operator import add
from langgraph.graph import START, END, StateGraph
from langgraph.store.memory import InMemoryStore
from uuid_extensions import uuid7

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

def invoke_graph(greeting: str, food_preference: str) -> None:
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

    # Define the Memory Store
    store = InMemoryStore()

    # Define the Namespace
    user_id = "1"
    memory_namespace = (user_id, "memories")

    # Add Memory to Store
    memory_id = str(uuid7())
    memory = {"food_preference": food_preference}
    store.put(memory_namespace, memory_id, memory)

    # Compile Graph
    graph = builder.compile(store=store)

    # Invoke Graph
    initial_state = State(nlist = [greeting])
    graph.invoke(initial_state)

    # Search Memory Store
    memories = store.search(memory_namespace)
    print(f"\n Memory Store: {memories[-1].dict()}")

