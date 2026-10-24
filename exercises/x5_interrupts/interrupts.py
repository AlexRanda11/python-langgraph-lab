from pydantic import BaseModel, Field
from typing import Annotated, Literal
from operator import add
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt

# Pydantic State Schema
class State(BaseModel):
    nlist: Annotated[list[str], add] = Field(default_factory=list)

# Node Definitions
def node_a(state: State) -> State:
    print(f"\nHello from Node A! Receiving: {state.nlist}")
    return State(nlist=["A"])

def node_b(state: State) -> State:
    print(f"\nHello from Node B! Receiving: {state.nlist}")
    return State(nlist=["B"])

def node_c(
    state: State,
) -> Command[Literal["node_a", "node_b", "node_x", "__end__"]]:
    # Map the Node to the Graph Index
    destinations: dict[str, Literal["node_a", "node_b", "node_x", "__end__"]] = {
        "A": "node_a",
        "B": "node_b",
        "X": "node_x",
        "Q": "__end__",
    }

    # If Choice not in Node List, Interrupt
    choice = state.nlist[-1].strip().upper()
    if choice not in destinations:
        response = interrupt(
            f"Unexpected input '{state.nlist[-1]}'. "
            "Please enter A, B, X, or Q. "
            "Enter 'continue' to visit Node A instead.\n"
        )
        choice = response.strip().upper() if isinstance(response, str) else ""
        if choice == "CONTINUE":
            choice = "A"
        elif choice not in destinations:
            print("No valid route selected; quitting.")
            choice = "Q"

    # Route to Specified Node
    return Command(
        update=State(nlist=["C", choice]),
        goto=destinations[choice],
    )

def node_x(state: State) -> State:
    print(f"\nHello from Node X! Receiving: {state.nlist}")
    return State(nlist=["X"])

def invoke_graph(greeting: str) -> None:
    # StateGraph Builder
    builder = StateGraph(State, input_schema=State)

    # Add Nodes
    builder.add_node("node_a", node_a)
    builder.add_node("node_b", node_b)
    builder.add_node("node_c", node_c)
    builder.add_node("node_x", node_x)

    # Add Edges
    builder.add_edge(START, "node_c")
    builder.add_edge("node_a", END)
    builder.add_edge("node_b", END)
    builder.add_edge("node_x", END)

    # Configure Checkpointer
    checkpointer = InMemorySaver()
    config: RunnableConfig = {"configurable": {"thread_id": "1"}}

    # Compile Graph
    graph = builder.compile(checkpointer=checkpointer)

    # Initialise the State
    initial_state = [greeting]

    # Agent Loop
    while True:
        # Prompt the Human
        choice = input(
            "\nYou are at Node C. Where would you like to go?\n\n"
            "A ---> Node A\n"
            "B ---> Node B\n"
            "X ---> Node X\n"
            "Q ---> Quit\n\n> "
        )

        # Invoke the Graph
        input_state = State(nlist=initial_state + [choice])
        result = graph.invoke(input_state, config=config)
        initial_state = []

        # Handle an Interrupt
        if result.get("__interrupt__"):
            pending_interrupt = result["__interrupt__"][0]
            response = input(f"\n{pending_interrupt.value}\n> ")
            result = graph.invoke(Command(resume=response), config=config)

        # Break the Loop
        if result["nlist"][-1] == "Q":
            break