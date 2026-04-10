"""
CLI & Interactive Runner for Gift Recommendation Agent
=======================================================
Run: python run.py
Or:  python run.py --query "Need a birthday gift for my wife, budget $100, she loves cooking"
"""

import argparse
import os
import sys
from typing import Optional
from langchain_core.messages import HumanMessage, AIMessage
from agent import run_conversation_turn, REQUIRED_FIELDS


# ── Example queries ──
EXAMPLE_QUERIES = [
    "Need a birthday gift for my wife, budget $100, she loves cooking",
    "Looking for a wedding gift for my colleague, around $50",
    "Christmas gift for my teenage son who's into gaming",
    "Mother's Day gift for my mom, she loves gardening",
    "Housewarming gift for a friend, budget $75",
]


def check_env():
    """Validate required API keys are set."""
    missing = []
    for key in ["OPENAI_API_KEY", "TAVILY_API_KEY"]:
        if not os.environ.get(key):
            missing.append(key)
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        print("\nSet them with:")
        for key in missing:
            print(f"  export {key}=your_key_here")
        sys.exit(1)


def get_display_name(field: str) -> str:
    """Convert field name to display name."""
    display_names = {
        "recipient_relationship": "Who it's for",
        "occasion": "Occasion",
        "budget_range": "Budget",
        "recipient_interests": "Interests",
        "recipient_age_group": "Age group",
        "special_requirements": "Special requirements"
    }
    return display_names.get(field, field)


def print_collected_info(state: dict):
    """Print currently collected information."""
    print("\n📋 **Current Information:**")
    print("-" * 40)
    for field in REQUIRED_FIELDS:
        value = state.get(field)
        display_name = get_display_name(field)
        status = f"✅ {value}" if value else "❌ Not provided"
        print(f"  {display_name}: {status}")

    # Optional fields
    for field in ["recipient_age_group", "special_requirements"]:
        value = state.get(field)
        if value:
            display_name = get_display_name(field)
            print(f"  {display_name}: ✅ {value}")
    print("-" * 40)


def interactive_mode():
    """Interactive conversation mode with human-in-the-loop."""
    print("\n🎁 Gift Recommendation Agent")
    print("=" * 50)
    print("I'll help you find the perfect gift!")
    print("I'll ask you questions to understand what you need.")
    print("Type 'exit' to quit, 'info' to see collected info, 'demo' for examples.\n")

    # Conversation state
    state = {
        "messages": [],
        "recipient_relationship": None,
        "occasion": None,
        "budget_range": None,
        "recipient_interests": None,
        "recipient_age_group": None,
        "special_requirements": None,
    }

    turn_count = 0
    max_turns = 15  # Prevent infinite loops

    while turn_count < max_turns:
        try:
            user_input = input("\n💬 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye! Happy gifting! 🎁")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("\nGoodbye! Happy gifting! 🎁")
            break

        if user_input.lower() == "info":
            print_collected_info(state)
            continue

        if user_input.lower() == "demo":
            run_demo()
            continue

        turn_count += 1

        print("\n🤖 Processing...")

        try:
            # Run one conversation turn
            result = run_conversation_turn(user_input, state)

            # Check if we have a question for the user
            if result.get("current_question") and not result.get("conversation_complete"):
                question = result["current_question"]
                print(f"\n🤖 {question}")

            # Check if we have recommendations
            elif result.get("final_response"):
                print("\n" + "=" * 60)
                print("🎁 GIFT RECOMMENDATIONS")
                print("=" * 60)
                print(result["final_response"])
                print("=" * 60)

                # Ask if user wants more recommendations
                try:
                    follow_up = input("\n💬 Want different recommendations? (yes/no): ").strip()
                    if follow_up.lower() in ["yes", "y"]:
                        clarification = input("💬 What should I adjust? ").strip()
                        if clarification:
                            # Continue conversation with refinement
                            result = run_conversation_turn(clarification, state)
                            if result.get("final_response"):
                                print("\n" + "=" * 60)
                                print(result["final_response"])
                                print("=" * 60)
                            continue
                except (EOFError, KeyboardInterrupt):
                    break

                print("\n✅ Recommendations complete! Happy gifting! 🎁")
                break

            else:
                # Unexpected state
                print("\n🤖 Hmm, let me think about that...")
                print("Please provide more details about the gift you're looking for.")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'exit' to quit.")

    if turn_count >= max_turns:
        print("\n⚠️ Maximum conversation length reached.")


def run_demo():
    """Run demo queries showing the conversation flow."""
    print("\n🎬 Running Demo — Gift Recommendation Flow\n")

    demo_conversation = [
        ("Need a birthday gift", "Initial vague request - agent should ask for details"),
        ("For my spouse", "Providing relationship"),
        ("It's for their 30th birthday", "Providing occasion"),
        ("Around $150", "Providing budget"),
        ("They love photography", "Providing interests"),
    ]

    print("This demo shows how the agent gathers information step by step.\n")

    state = {
        "messages": [],
        "recipient_relationship": None,
        "occasion": None,
        "budget_range": None,
        "recipient_interests": None,
        "recipient_age_group": None,
        "special_requirements": None,
    }

    for i, (query, note) in enumerate(demo_conversation, 1):
        print(f"\n{'─' * 60}")
        print(f"📌 Step {i}: {note}")
        print(f"💬 You: {query}")
        print('─' * 60)

        try:
            result = run_conversation_turn(query, state)

            if result.get("current_question") and not result.get("conversation_complete"):
                print(f"\n🤖 {result['current_question']}")
                print("\n[Collecting more info...]")

            elif result.get("final_response"):
                print("\n🎁 **Recommendations Generated!**")
                print(result["final_response"][:500] + "...\n")
                print("(Full recommendations shown in real usage)")
                break

        except Exception as e:
            print(f"\n❌ Error at step {i}: {e}")
            break

        input("\nPress Enter for next step...")

    print("\n" + "=" * 60)
    print("Demo complete! Run in interactive mode to get your own recommendations.")
    print("=" * 60)


def run_single_query(query: str):
    """Run a single query (might need multiple turns)."""
    print(f"\n💬 Query: {query}\n")

    state = {
        "messages": [],
        "recipient_relationship": None,
        "occasion": None,
        "budget_range": None,
        "recipient_interests": None,
        "recipient_age_group": None,
        "special_requirements": None,
    }

    for turn in range(10):
        try:
            result = run_conversation_turn(query, state)

            if result.get("current_question") and not result.get("conversation_complete"):
                print(f"\n🤖 {result['current_question']}")
                try:
                    user_response = input("\n💬 Your response: ").strip()
                    if not user_response:
                        continue
                    query = user_response  # Use as next query
                except (EOFError, KeyboardInterrupt):
                    break

            elif result.get("final_response"):
                print("\n" + "=" * 60)
                print(result["final_response"])
                print("=" * 60)
                break

        except Exception as e:
            print(f"\n❌ Error: {e}")
            break


def main():
    parser = argparse.ArgumentParser(description="Gift Recommendation Agent")
    parser.add_argument("--query", "-q", type=str, help="Single query to run")
    parser.add_argument("--demo", "-d", action="store_true", help="Run demo conversation")
    args = parser.parse_args()

    check_env()

    if args.demo:
        run_demo()
    elif args.query:
        run_single_query(args.query)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
