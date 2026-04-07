from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import RetryPolicy
from langgraph.graph import StateGraph, START, END
from states import TravelBookingState
from nodes import (
    parse_request,
    classify_intent,
    extract_details,
    search_flights,
    search_hotels,
    search_packages,
    present_options,
    human_review,
    confirm_booking,
    human_agent
)

# Create the graph
workflow = StateGraph(TravelBookingState)

# Add nodes
workflow.add_node("parse_request", parse_request)
workflow.add_node("classify_intent", classify_intent)
workflow.add_node("extract_details", extract_details)
workflow.add_node(
    "search_flights",
    search_flights,
    retry_policy=RetryPolicy(max_attempts=3)
)
workflow.add_node(
    "search_hotels",
    search_hotels,
    retry_policy=RetryPolicy(max_attempts=3)
)
workflow.add_node(
    "search_packages",
    search_packages,
    retry_policy=RetryPolicy(max_attempts=3)
)
workflow.add_node("present_options", present_options)
workflow.add_node("human_review", human_review)
workflow.add_node("confirm_booking", confirm_booking)
workflow.add_node("human_agent", human_agent)

# Add edges
workflow.add_edge(START, "parse_request")
workflow.add_edge("parse_request", "classify_intent")
workflow.add_edge("confirm_booking", END)
workflow.add_edge("human_agent", END)

# Compile with checkpointer for persistence
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
