from exercises.x1_static_edges.static_edges import invoke_graph as x1_invoke_graph
from exercises.x2_conditional_edges.conditional_edges import invoke_graph as x2_invoke_graph
from exercises.x3_checkpoints.checkpoints import invoke_graph as x3_invoke_graph
from exercises.x4_memory_store.memory_store import invoke_graph as x4_invoke_graph
from exercises.x5_interrupts.interrupts import invoke_graph as x5_invoke_graph
from exercises.x6_streaming.streaming import invoke_graph as x6_invoke_graph
from exercises.x7_entrypoints.entrypoints import invoke_workflow as x7_invoke_workflow

def main():
    print("\n====================== Welcome to LangGraph ======================\n")

    greeting = "Hello there!"
    food_preference = "I like pizza!"
    joke_topic = "potatoes"
    essay_topic = "the history of flight"
    print(f"Human Message: {greeting}")
    print(f"Human Preference: {food_preference}")
    print(f"Joke Topic: {joke_topic}")
    print(f"Essay Topic: {essay_topic}")

    choice = input("""\nPlease enter from the following choices:\n
        1. Static Edges
        2. Conditional Edges
        3. Checkpoints
        4. Memory Store
        5. Interrupts
        6. Streaming
        7. Entrypoints\n\n> """)
    print(f"\nHuman Choice: {choice}")

    match choice:
        case "1":
            # Invoke Static Edges Graph
            print("\n========================== Static Edges ==========================\n")
            x1_invoke_graph(greeting=greeting)
        case "2":
            # Invoke Conditional Edges Graph
            print("\n======================= Conditional Edges ========================\n")
            x2_invoke_graph(greeting=greeting)
        case "3":
            # Invoke Checkpoints Graph
            print("\n========================== Checkpoints ===========================\n")
            x3_invoke_graph(greeting=greeting)
        case "4":
            # Invoke Memory Graph
            print("\n========================== Memory Store ==========================\n")
            x4_invoke_graph(greeting=greeting, food_preference=food_preference)
        case "5":
            print("\n=========================== Interrupts ===========================\n")
            x5_invoke_graph(greeting=greeting)
        case "6":
            print("\n=========================== Streaming ============================\n")
            x6_invoke_graph(joke_topic=joke_topic)
        case "7":
            print("\n========================== Entrypoints ===========================\n")
            x7_invoke_workflow(essay_topic=essay_topic)

    print("\n=========================== Toodle Pip! ==========================\n")

if __name__ == "__main__":
    main()