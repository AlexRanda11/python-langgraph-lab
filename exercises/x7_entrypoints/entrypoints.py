from langchain_core.runnables import RunnableConfig
from langchain_core.utils.uuid import uuid7
from langchain.chat_models import init_chat_model
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import InMemorySaver

model = init_chat_model('gpt-5.4-mini')

# Task: Generate Essay using an LLM
@task
def compose_essay(topic: str) -> str:
    """Generate essay text from either a string or content-block response."""
    content = model.invoke([
        {"role": "system", "content": "You are a helpful assistant that writes essays."},
        {"role": "user", "content": f"Write an essay about {topic}."}
    ]).text
    if not content:
        raise ValueError("Expected the model to return text content.")
    return content

# Create a Checkpointer for Persistence
checkpointer = InMemorySaver()

# Define the Entrypoint
@entrypoint(checkpointer=checkpointer)
def workflow(topic: str) -> str:
    """Simple workflow that generates an essay with an LLM."""
    return compose_essay(topic).result()

# Execute the Workflow
def invoke_workflow(essay_topic: str):
    config: RunnableConfig = {"configurable": {"thread_id": str(uuid7())}}
    # Stream the Results
    for chunk in workflow.stream(
        essay_topic,
        config=config,
        stream_mode="values",
        version="v2",
    ):
        if chunk["type"] == "values":
            print(f"values: {chunk['data']}")