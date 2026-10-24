# Python LangGraph Lab

A hands-on collection of seven Python exercises demonstrating core **LangGraph**
components, from building stateful graphs to running LLM-backed workflows.

## What the lab contains

- **Interactive launcher:** [main.py](main.py) lets you choose an exercise from a
  numbered menu and supplies sample greetings, preferences, and topics.
- **Graph fundamentals:** Pydantic state schemas, reducers, parallel branches,
  static edges, and conditional routing.
- **State and human interaction:** in-memory checkpoints, a namespaced memory
  store, and interrupt/resume flows.
- **LLM workflows:** streamed joke generation using the Graph API and essay
  generation using the Functional API.
- **Reference artefacts:** saved graph diagrams for exercises 1-3 and sample
  console logs for all seven exercises.
- **Environment setup:** [pyproject.toml](pyproject.toml) declares dependencies,
  [uv.lock](uv.lock) locks them, and [.python-version](.python-version) selects
  Python 3.11.

## Directory tree

```text
.
|-- README.md
|-- main.py                         # Interactive exercise selector
|-- pyproject.toml                  # Project metadata and dependencies
|-- uv.lock                         # Locked dependency versions
|-- .python-version                # Default Python version
|-- .gitignore
|-- .vscode/                        # Editor settings
`-- exercises/
    |-- __init__.py
    |-- x1_static_edges/             # Build a graph with static edges
    |   |-- static_edges.py
    |   |-- graph.png
    |   `-- graph_response.log
    |-- x2_conditional_edges/        # Route between nodes conditionally
    |   |-- conditional_edges.py
    |   |-- graph.png
    |   `-- graph_response.log
    |-- x3_checkpoints/              # Save and inspect graph checkpoints
    |   |-- checkpoints.py
    |   |-- graph.png
    |   `-- graph_response.log
    |-- x4_memory_store/             # Store and retrieve long-term memory
    |   |-- memory_store.py
    |   `-- graph_response.log
    |-- x5_interrupts/               # Pause for human input and resume
    |   |-- interrupts.py
    |   `-- graph_response.log
    |-- x6_streaming/                # Stream LLM message chunks
    |   |-- streaming.py
    |   `-- graph_response.log
    `-- x7_entrypoints/              # Run a task-based workflow
        |-- entrypoints.py
        `-- graph_response.log
```

Each exercise directory also contains an `__init__.py` package marker, omitted
above for readability. Local environment files and generated caches are not shown.

## Exercises

The numbers match the launcher menu. Follow them in order for a gradual
introduction, or select a specific topic.

| # | Exercise | Concepts demonstrated | What it does |
|---|----------|-----------------------|--------------|
| 1 | [Static edges](exercises/x1_static_edges/static_edges.py) | `StateGraph`, Pydantic state, custom list reducer, fan-out/fan-in | Runs A and B in parallel, combines their state updates, then runs C and ends. Prints the state received by each node. |
| 2 | [Conditional edges](exercises/x2_conditional_edges/conditional_edges.py) | State-based routing with `add_conditional_edges` | Extends the first graph with a router after C. Routes to X when the last state entry is `"C"` (the default path), otherwise ends. |
| 3 | [Checkpoints](exercises/x3_checkpoints/checkpoints.py) | `InMemorySaver`, `thread_id`, `get_state` | Runs the A/B/C graph with checkpointing and prints the resulting state snapshot for thread `"1"`. |
| 4 | [Memory store](exercises/x4_memory_store/memory_store.py) | `InMemoryStore`, namespaces, UUID memory keys, `put`/`search` | Stores a food preference under a user's memory namespace, runs the graph, then retrieves and prints the stored item. |
| 5 | [Interrupts](exercises/x5_interrupts/interrupts.py) | Human-in-the-loop interaction, `interrupt`, `Command`, checkpointed resume | Prompts for A, B, X, or Q at node C. Invalid input pauses for clarification; `continue` selects A. Resumes with the supplied answer and repeats until Q. |
| 6 | [Streaming](exercises/x6_streaming/streaming.py) | Graph API, chat model invocation, `messages` streaming, v2 events | Uses OpenAI's `gpt-5.4-mini` to generate a joke and prints incoming message content chunks separated by `\|`. |
| 7 | [Entrypoints](exercises/x7_entrypoints/entrypoints.py) | Functional API, `@task`, `@entrypoint`, checkpointing, `values` streaming | Uses `gpt-5.4-mini` to compose an essay, waits for the task result, and prints workflow values rather than token-by-token output. |

Exercises 1-5 do not make LLM calls. The checkpoint and memory examples use
**in-memory storage only**: they do not persist data across process restarts.
Exercise 4 demonstrates storing and retrieving a record; its graph nodes do not
read that preference.

## Getting started

### Prerequisites

- Python **3.11 or newer**.
- [uv](https://docs.astral.sh/uv/) for dependency and environment management.
- An OpenAI API key with access to `gpt-5.4-mini` for exercises 6-7. These
  exercises make API calls and may incur charges.

Run the following from the repository root:

```bash
uv sync
```

Create a local `.env` file in the repository root containing your key:

```dotenv
OPENAI_API_KEY=your-openai-api-key
```

The repository ignores `.env` files; do not commit credentials.
The launcher imports every exercise and initializes both chat models before
displaying the menu, so configure the key even when selecting exercises 1-5.

The first three exercises currently export diagrams to legacy `examples/`
paths. Create their output directories before running them:

```bash
mkdir -p examples/static_edges examples/conditional_edges examples/checkpoints
```

Start the menu with the environment file loaded explicitly:

```bash
uv run --env-file .env main.py
```

Choose **1-7**. The launcher runs one selected exercise, then exits; exercise 5
has its own interactive loop, which you exit with **Q**. To change the sample
inputs, edit the greeting, food preference, joke topic, or essay topic in
[main.py](main.py).

### Output and implementation notes

- Exercises print their results to the terminal. Committed sample logs are
  available for [static edges](exercises/x1_static_edges/graph_response.log),
  [conditional edges](exercises/x2_conditional_edges/graph_response.log),
  [checkpoints](exercises/x3_checkpoints/graph_response.log),
  [memory store](exercises/x4_memory_store/graph_response.log), and
  [interrupts](exercises/x5_interrupts/graph_response.log),
  [streaming](exercises/x6_streaming/graph_response.log), and
  [entrypoints](exercises/x7_entrypoints/graph_response.log). These are sample
  runs, not fixed expected output: model-generated text can vary, and the
  checkpoint and memory-store logs include generated timestamps and IDs.
- The saved diagrams are available for
  [static edges](exercises/x1_static_edges/graph.png),
  [conditional edges](exercises/x2_conditional_edges/graph.png), and
  [checkpoints](exercises/x3_checkpoints/graph.png).
  The active `draw_mermaid_png` calls write to the legacy paths described above,
  not these committed files, and use an external Mermaid rendering service by
  default. Rendering therefore requires network access.
- The explicit `--env-file .env` flag loads the root environment file for both
  LLM exercises. The streaming module's own dotenv loader instead targets
  `exercises/.env`.
- The exercise modules expose callable functions but do not have standalone
  script entry points; use the launcher to run them.