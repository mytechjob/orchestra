from typing import Literal
from langgraph.graph import END
from langgraph.types import interrupt, Command
from langchain.messages import HumanMessage
from states import ContentModerationState, ContentClassification
from llm import llm

def ingest_content(state: ContentModerationState) -> dict:
    """Log incoming content for moderation"""
    return {
        "messages": [HumanMessage(content=f"Moderating {state['content_type']}: {state['content_text'][:100]}...")]
    }

def classify_content(state: ContentModerationState) -> Command[Literal["analyze_toxicity", "analyze_spam", "direct_action"]]:
    """Use LLM to classify content and determine initial risk level"""

    structured_llm = llm.with_structured_output(ContentClassification)

    author_context = ""
    if state.get('author_history'):
        author_context = f"""
        Author History:
        - Previous violations: {state['author_history'].get('violations', 0)}
        - Account age: {state['author_history'].get('account_age_days', 'unknown')} days
        - Trust score: {state['author_history'].get('trust_score', 'unknown')}
        """

    classification_prompt = f"""
    Analyze this user-generated content for moderation:

    Content Type: {state['content_type']}
    Content: {state['content_text']}
    {author_context}

    Classify the content into categories: safe, spam, inappropriate, hate_speech, misinformation, copyright, or nsfw.
    Provide confidence score (0.0-1.0), severity level, and list any flagged terms.
    """

    classification = structured_llm.invoke(classification_prompt)

    # Route based on classification
    if classification['category'] == 'safe' and classification['confidence'] > 0.9:
        goto = "direct_action"
    elif classification['category'] in ['hate_speech', 'copyright']:
        goto = "direct_action"  # Auto-reject these
    elif classification['category'] == 'spam':
        goto = "analyze_spam"
    else:
        goto = "analyze_toxicity"

    return Command(
        update={"classification": classification},
        goto=goto
    )

def analyze_toxicity(state: ContentModerationState) -> Command[Literal["direct_action", "human_review"]]:
    """Deep analyze content for toxicity, bias, or harmful language"""

    classification = state.get('classification', {})

    toxicity_prompt = f"""
    Analyze the toxicity level of this content:

    Content: {state['content_text']}
    Initial Classification: {classification.get('category', 'unknown')}
    Flagged Terms: {classification.get('flagged_terms', [])}

    Provide:
    1. Toxicity score (0.0-1.0)
    2. Specific concerns or context notes
    3. Recommended action: approve, reject, flag_for_review, or quarantine
    """

    response = llm.invoke(toxicity_prompt)

    # Parse response (in production, use structured output)
    toxicity_score = 0.5  # Placeholder - parse from response
    action = "flag_for_review"  # Default for toxic content

    return Command(
        update={
            "toxicity_score": toxicity_score,
            "context_notes": response.content,
            "action": action
        },
        goto="human_review" if toxicity_score > 0.6 else "direct_action"
    )

def analyze_spam(state: ContentModerationState) -> Command[Literal["direct_action"]]:
    """Check for spam indicators like links, repetitive content, promotional language"""

    content = state['content_text'].lower()

    # Rule-based spam detection
    spam_indicators = []
    if 'http' in content or 'www.' in content:
        spam_indicators.append("contains_links")
    if len(content) < 20:
        spam_indicators.append("very_short_content")
    if content.count('!') > 3:
        spam_indicators.append("excessive_punctuation")
    if any(word in content for word in ['buy now', 'click here', 'limited offer', 'free money']):
        spam_indicators.append("promotional_language")

    # Determine action based on spam indicators
    if len(spam_indicators) >= 2:
        action = "reject"
    elif len(spam_indicators) == 1:
        action = "flag_for_review"
    else:
        action = "approve"

    return Command(
        update={
            "spam_indicators": spam_indicators,
            "action": action
        },
        goto="direct_action"
    )

def direct_action(state: ContentModerationState) -> Command[Literal["publish", "human_review", "remove_content"]]:
    """Execute automatic moderation decision or escalate to human review"""

    classification = state.get('classification', {})
    action = state.get('action')

    # Auto-decide if not already set
    if not action:
        category = classification.get('category', 'safe')
        severity = classification.get('severity', 'low')
        confidence = classification.get('confidence', 0.5)

        if category == 'safe' and confidence > 0.9:
            action = "approve"
        elif category in ['hate_speech', 'copyright'] or severity == 'critical':
            action = "reject"
        elif severity in ['high', 'critical'] or confidence < 0.7:
            action = "flag_for_review"
        else:
            action = "approve"

    # Route based on action
    if action == "approve":
        goto = "publish"
    elif action == "reject":
        goto = "remove_content"
    else:
        goto = "human_review"

    return Command(
        update={"action": action},
        goto=goto
    )

def human_review(state: ContentModerationState) -> Command[Literal["publish", "remove_content", END]]:
    """Pause for human moderator review"""

    classification = state.get('classification', {})

    review_data = interrupt({
        "content_id": state.get('content_id', ''),
        "content_type": state.get('content_type', ''),
        "content_text": state.get('content_text', ''),
        "classification": classification.get('category', 'unknown'),
        "confidence": classification.get('confidence', 0),
        "severity": classification.get('severity', 'unknown'),
        "toxicity_score": state.get('toxicity_score'),
        "spam_indicators": state.get('spam_indicators', []),
        "recommended_action": state.get('action', 'unknown'),
        "context_notes": state.get('context_notes', ''),
        "action": "Please review and decide: approve, reject, or quarantine"
    })

    # Process human decision
    decision = review_data.get('decision', 'approve')
    moderator_notes = review_data.get('notes', '')

    if decision == 'approve':
        goto = "publish"
    elif decision in ['reject', 'quarantine']:
        goto = "remove_content"
    else:
        # Human takes over externally
        goto = END

    return Command(
        update={
            "review_decision": review_data,
            "moderator_notes": moderator_notes,
            "action": decision
        },
        goto=goto
    )

def publish(state: ContentModerationState) -> dict:
    """Approve and publish the content"""
    print(f"[PUBLISH] Content {state['content_id']} approved and published")
    return {"action": "approved"}

def remove_content(state: ContentModerationState) -> dict:
    """Remove/reject the content and optionally notify author"""
    print(f"[REMOVE] Content {state['content_id']} rejected and removed")
    print(f"Reason: {state.get('moderator_notes', state.get('context_notes', 'Policy violation'))}")
    return {"action": "rejected"}
