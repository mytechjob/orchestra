from dotenv import load_dotenv
load_dotenv()
from agent import app
from langgraph.types import Command
import os

def run_moderation_interactive():
    """Run content moderation with interactive CLI input"""
    print("🚀 Content Moderation Agent - Interactive Mode")
    print(f"{'='*60}")

    # Get content details from user
    content_id = input("\n📝 Enter Content ID (e.g., post_001): ").strip()
    if not content_id:
        content_id = f"post_{hash(str(os.getpid())) % 10000:04d}"

    content_text = input("\n📄 Enter content text: ").strip()
    if not content_text:
        print("❌ Content cannot be empty!")
        return

    print("\n📋 Content Types: post, comment, review, image_caption, video_description")
    content_type = input("📝 Enter content type (default: post): ").strip() or "post"

    author_id = input("📝 Enter Author ID (e.g., user_123): ").strip() or "anonymous"

    # Get author history
    print("\n--- Author History (optional, press Enter to skip) ---")
    try:
        violations = int(input("⚠️  Previous violations (default: 0): ").strip() or "0")
        account_age = int(input("📅 Account age in days (default: unknown/0): ").strip() or "0")
        trust_score = float(input("⭐ Trust score 0.0-1.0 (default: 0.5): ").strip() or "0.5")
    except ValueError:
        print("⚠️  Invalid input, using defaults")
        violations = 0
        account_age = 0
        trust_score = 0.5

    author_history = {
        "violations": violations,
        "account_age_days": account_age,
        "trust_score": trust_score
    }

    # Initialize state
    initial_state = {
        "content_id": content_id,
        "content_text": content_text,
        "content_type": content_type,
        "author_id": author_id,
        "author_history": author_history,
        "messages": []
    }

    config = {"configurable": {"thread_id": f"thread_{content_id}"}}
    
    print(f"\n{'='*60}")
    print("⚙️  Processing content...")
    print(f"{'='*60}")
    
    result = app.invoke(initial_state, config)

    # Check if human review is needed
    interrupts = result.get('__interrupt__')
    if interrupts:
        # LangGraph returns interrupts as a list
        interrupt_data = interrupts[0].value if hasattr(interrupts[0], 'value') else interrupts[0]
        
        print(f"\n{'='*60}")
        print("⚠️  Content flagged for HUMAN REVIEW")
        print(f"{'='*60}")

        # Display review information
        print(f"\n📋 Content ID: {interrupt_data.get('content_id', '')}")
        print(f"📄 Content Type: {interrupt_data.get('content_type', '')}")
        print(f"\n📝 Content:\n   {interrupt_data.get('content_text', '')}")
        print(f"\n🏷️  Classification: {interrupt_data.get('classification', '')}")
        print(f"📊 Confidence: {interrupt_data.get('confidence', 0)}")
        print(f"🚨 Severity: {interrupt_data.get('severity', '')}")

        if interrupt_data.get('toxicity_score') is not None:
            print(f"☠️  Toxicity Score: {interrupt_data.get('toxicity_score')}")

        if interrupt_data.get('spam_indicators'):
            print(f"🗑️  Spam Indicators: {', '.join(interrupt_data.get('spam_indicators', []))}")

        print(f"\n🎯 Recommended Action: {interrupt_data.get('recommended_action', '')}")

        if interrupt_data.get('context_notes'):
            print(f"\n📝 Context Notes:\n   {interrupt_data.get('context_notes', '')}")

        # Get human decision
        print(f"\n{'='*60}")
        print("👤 MODERATOR DECISION")
        print(f"{'='*60}")
        print("Options: approve, reject, quarantine, skip")
        decision = input("\nEnter your decision: ").strip().lower()
        
        if decision in ['approve', 'reject', 'quarantine']:
            notes = input("📝 Add notes (optional): ").strip()

            # Resume with human decision
            human_response = Command(
                resume={
                    "decision": decision,
                    "notes": notes if notes else f"Moderator {decision}d content"
                }
            )

            print(f"\n⚙️  Processing your decision...")
            final_result = app.invoke(human_response, config)
            print(f"✅ Final action: {final_result.get('action', 'unknown')}")
        else:
            print("⏭️  Skipping - content remains in pending state")
    else:
        action = result.get('action', 'unknown')
        print(f"\n✅ Auto-moderated: {action}")
        if action == 'approved':
            print("📝 Content published successfully")
        elif action == 'rejected':
            print("🗑️  Content removed due to policy violation")

    return result

# Run interactive moderation
run_moderation_interactive()

# Ask if user wants to continue
while input("\n🔄 Moderate another content? (y/n): ").strip().lower() == 'y':
    run_moderation_interactive()

print(f"\n{'='*60}")
print("👋 Content Moderation Agent - Session Ended")
print(f"{'='*60}")

# Generate and save the agent graph visualization
graph_image_path = os.path.join(os.path.dirname(__file__), "agent_graph.png")
graph_png = app.get_graph().draw_mermaid_png()
with open(graph_image_path, "wb") as f:
    f.write(graph_png)
print(f"\n📊 Agent graph saved to: {graph_image_path}")
