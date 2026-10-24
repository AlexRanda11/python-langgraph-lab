from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START

# Load OpenAI API Key from .env File
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Define State Schema
class MyState(BaseModel):
    topic: str
    joke: str = ""

# Define LLM Model
model = init_chat_model(model="gpt-5.4-mini")

# Define Node that Invokes Model
def call_model(state: MyState):
    """Call the LLM to generate a joke about a topic"""
    # Note that message events are emitted even when the
    # LLM is run using .invoke rather than .stream
    model_response = model.invoke([{
        "role": "user",
        "content": f"Generate a joke about {state.topic}"
    }])
    return {"joke": model_response.content}

def invoke_graph(joke_topic: str):
    # Define and Invoke the Graph
    graph = (
        StateGraph(MyState, input_schema=MyState)
        .add_node(call_model)
        .add_edge(START, "call_model")
        .compile()
    )
    # The "messages" stream mode streams LLM tokens with metadata.
    for chunk in graph.stream(
        MyState(topic=joke_topic),
        stream_mode="messages",
        version="v1",
    ):
        message_chunk, metadata = chunk
        if not isinstance(message_chunk, BaseMessage):
            raise TypeError("Expected a BaseMessage from the messages stream")
        if message_chunk.content:
            print(message_chunk.content, end="|", flush=True)
    print()