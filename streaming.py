from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

class MyState(BaseModel):
    topic: str
    joke: str = ""

model = init_chat_model(model="gpt-5.4-mini")

def call_model(state: MyState):
    """Call the LLM to generate a joke about a topic"""
    model_response = model.invoke([{
        "role": "user",
        "content": f"Generate a joke about {state.topic}"
    }])
    return {"joke": model_response.content}

def invoke_graph(joke_topic: str):
    graph = (
        StateGraph(MyState, input_schema=MyState)
        .add_node(call_model)
        .add_edge(START, "call_model")
        .compile()
    )
    for chunk in graph.stream(
        MyState(topic=joke_topic),
        stream_mode="messages",
        version="v2",
    ):
        if chunk["type"] == "messages":
            message_chunk, metadata = chunk["data"]
            if message_chunk.content:
                print(message_chunk.content, end="|", flush=True)
    print()