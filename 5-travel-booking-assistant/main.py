from dotenv import load_dotenv
load_dotenv()
from agent import app
from langgraph.types import Command
import os

# Test cases covering different travel booking scenarios
test_requests = [
    {
        "user_id": "user_001",
        "request_text": "I need a flight from New York to Los Angeles on May 1st, returning May 5th for 2 people",
        "conversation_history": [],
        "description": "Simple flight search - auto-book"
    },
    {
        "user_id": "user_002",
        "request_text": "Find me a luxury hotel in Paris for a week, budget is $5000, I want 5-star with spa",
        "conversation_history": [],
        "description": "High-budget hotel search - needs human review"
    },
    {
        "user_id": "user_003",
        "request_text": "I want to book a complete vacation package to Tokyo, flights + hotel, mid-range budget",
        "conversation_history": [],
        "description": "Package deal search - auto-book"
    },
    {
        "user_id": "user_004",
        "request_text": "I need to cancel my booking for next week due to emergency",
        "conversation_history": [],
        "description": "Cancellation request - escalate to agent"
    },
    {
        "user_id": "user_005",
        "request_text": "Can you help me plan a honeymoon trip to Maldives? Something premium and memorable",
        "conversation_history": [],
        "description": "Complex inquiry - escalate to agent"
    }
]

def run_booking(request_case):
    """Run a single booking test case"""
    print(f"\n{'='*60}")
    print(f"Testing: {request_case['description']}")
    print(f"User: {request_case['user_id']}")
    print(f"{'='*60}")
    print(f"Request: {request_case['request_text']}")

    initial_state = {
        "user_id": request_case["user_id"],
        "request_text": request_case["request_text"],
        "conversation_history": request_case["conversation_history"],
        "messages": []
    }

    config = {"configurable": {"thread_id": f"thread_{request_case['user_id']}"}}
    result = app.invoke(initial_state, config)

    # Check if human review is needed
    if result.get('__interrupt__'):
        print(f"\n⚠️  Booking flagged for AGENT REVIEW")
        print(f"Review data: {result['__interrupt__']}")

        # Simulate agent approval
        agent_response = Command(
            resume={
                "approved": True,
                "notes": "Approved by travel agent"
            }
        )

        final_result = app.invoke(agent_response, config)
        print(f"✅ Final status: {final_result.get('action', 'unknown')}")
    else:
        print(f"✅ Auto-processed: {result.get('action', 'unknown')}")
        if result.get('booking_confirmation'):
            print(f"🎫 Booking ID: {result['booking_confirmation']['booking_id']}")

    return result

# Run all test cases
print("✈️  Travel Booking Assistant - Test Suite")
for i, request_case in enumerate(test_requests):
    run_booking(request_case)

print(f"\n{'='*60}")
print("✅ All test cases completed!")
print(f"{'='*60}")

# Generate and save the agent graph visualization
graph_image_path = os.path.join(os.path.dirname(__file__), "agent_graph.png")
graph_png = app.get_graph().draw_mermaid_png()
with open(graph_image_path, "wb") as f:
    f.write(graph_png)
print(f"\n📊 Agent graph saved to: {graph_image_path}")
