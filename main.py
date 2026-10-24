from exercises.x1_static_edges.static_edges import invoke_graph as se_invoke_graph
from exercises.x2_conditional_edges.conditional_edges import invoke_graph as ce_invoke_graph
from exercises.x3_checkpoints.checkpoints import invoke_graph as cp_invoke_graph
from exercises.x4_memory_store.memory_store import invoke_graph as ms_invoke_graph
from exercises.x5_interrupts.interrupts import invoke_graph as ir_invoke_graph

def main():
    print("\n====================== Welcome to LangGraph ======================\n")
    greeting = "Hello there!"
    print(f"Human Message: {greeting}")
    food_preference = "I like pizza!"
    print(f"Human Preference: {food_preference}")

    choice = input("""\nPlease enter from the following choices:\n
        1. Static Edges
        2. Conditional Edges
        3. Checkpoints
        4. Memory Store
        5. Interrupts\n\n> """)
    print(f"\nHuman Choice: {choice}")

    match choice:
        case "1":
            # Invoke Static Edges Graph
            print("\n========================== Static Edges ==========================\n")
            se_invoke_graph(greeting=greeting)
        case "2":
            # Invoke Conditional Edges Graph
            print("\n======================= Conditional Edges ========================\n")
            ce_invoke_graph(greeting=greeting)
        case "3":
            # Invoke Checkpoints Graph
            print("\n========================== Checkpoints ===========================\n")
            cp_invoke_graph(greeting=greeting)
        case "4":
            # Invoke Memory Graph
            print("\n========================== Memory Store ==========================\n")
            ms_invoke_graph(greeting=greeting, food_preference=food_preference)
        case "5":
            print("\n=========================== Interrupts ===========================\n")
            ir_invoke_graph(greeting=greeting)


    print("\n=========================== Toodle Pip! ==========================\n")

if __name__ == "__main__":
    main()