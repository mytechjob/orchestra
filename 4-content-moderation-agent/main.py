from dotenv import load_dotenv
load_dotenv()
from agent import app
from langgraph.types import Command
import os

# Test cases covering different moderation scenarios
test_contents = [
    {
        "content_id": "post_001",
        "content_text": "Just had an amazing coffee at the new cafe downtown! Highly recommend their latte ☕",
        "content_type": "post",
        "author_id": "user_123",
        "author_history": {"violations": 0, "account_age_days": 365, "trust_score": 0.9},
        "description": "Safe content - should auto-approve"
    },
    {
        "content_id": "comment_002",
        "content_text": "BUY NOW!!! Limited offer! Click here for FREE MONEY!!! www.scam-link.com",
        "content_type": "comment",
        "author_id": "user_456",
        "author_history": {"violations": 3, "account_age_days": 2, "trust_score": 0.1},
        "description": "Obvious spam - should auto-reject"
    },
    {
        "content_id": "post_003",
        "content_text": "I think the new policy has some issues that need discussion. Here are my concerns...",
        "content_type": "post",
        "author_id": "user_789",
        "author_history": {"violations": 0, "account_age_days": 180, "trust_score": 0.7},
        "description": "Borderline content - needs human review"
    },
    {
        "content_id": "review_004",
        "content_text": "This product is terrible and anyone who buys it is an idiot.",
        "content_type": "review",
        "author_id": "user_321",
        "author_history": {"violations": 1, "account_age_days": 30, "trust_score": 0.4},
        "description": "Toxic content - should flag for review"
    },
    {
        "content_id": "caption_005",
        "content_text": "Check out my new YouTube video! Link in bio!",
        "content_type": "video_description",
        "author_id": "user_654",
        "author_history": {"violations": 0, "account_age_days": 90, "trust_score": 0.6},
        "description": "Mild promotional content - spam analysis"
    }
]

def run_moderation(test_case):
    """Run a single moderation test case"""
    print(f"\n{'='*60}")
    print(f"Testing: {test_case['description']}")
    print(f"Content ID: {test_case['content_id']}")
    print(f"{'='*60}")

    initial_state = {
        "content_id": test_case["content_id"],
        "content_text": test_case["content_text"],
        "content_type": test_case["content_type"],
        "author_id": test_case["author_id"],
        "author_history": test_case["author_history"],
        "messages": []
    }

    config = {"configurable": {"thread_id": f"thread_{test_case['content_id']}"}}
    result = app.invoke(initial_state, config)

    # Check if human review is needed
    if result.get('__interrupt__'):
        print(f"\n⚠️  Content flagged for HUMAN REVIEW")
        print(f"Interrupt data: {result['__interrupt__']}")

        # Simulate human approval
        human_response = Command(
            resume={
                "decision": "approve",
                "notes": "Reviewed and approved by moderator"
            }
        )

        final_result = app.invoke(human_response, config)
        print(f"✅ Final action: {final_result.get('action', 'unknown')}")
    else:
        print(f"✅ Auto-moderated: {result.get('action', 'unknown')}")

    return result

# Run all test cases
print("🚀 Content Moderation Agent - Test Suite")
for i, test_case in enumerate(test_contents):
    run_moderation(test_case)

print(f"\n{'='*60}")
print("✅ All test cases completed!")
print(f"{'='*60}")

# Generate and save the agent graph visualization
graph_image_path = os.path.join(os.path.dirname(__file__), "agent_graph.png")
graph_png = app.get_graph().draw_mermaid_png()
with open(graph_image_path, "wb") as f:
    f.write(graph_png)
print(f"\n📊 Agent graph saved to: {graph_image_path}")
