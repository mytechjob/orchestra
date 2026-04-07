from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import RetryPolicy
from langgraph.graph import StateGraph, START, END
from states import ContentModerationState
from nodes import (
    ingest_content,
    classify_content,
    analyze_toxicity,
    analyze_spam,
    direct_action,
    human_review,
    publish,
    remove_content
)

# Create the graph
workflow = StateGraph(ContentModerationState)

# Add nodes
workflow.add_node("ingest_content", ingest_content)
workflow.add_node("classify_content", classify_content)
workflow.add_node("analyze_toxicity", analyze_toxicity)
workflow.add_node(
    "analyze_spam",
    analyze_spam,
    retry_policy=RetryPolicy(max_attempts=2)
)
workflow.add_node("direct_action", direct_action)
workflow.add_node("human_review", human_review)
workflow.add_node("publish", publish)
workflow.add_node("remove_content", remove_content)

# Add edges
workflow.add_edge(START, "ingest_content")
workflow.add_edge("ingest_content", "classify_content")
workflow.add_edge("publish", END)
workflow.add_edge("remove_content", END)

# Compile with checkpointer for persistence
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
