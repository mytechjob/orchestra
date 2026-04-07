from typing import TypedDict, Literal

# Define the structure for content classification
class ContentClassification(TypedDict):
    category: Literal["safe", "spam", "inappropriate", "hate_speech", "misinformation", "copyright", "nsfw"]
    confidence: float  # 0.0 to 1.0
    severity: Literal["low", "medium", "high", "critical"]
    flagged_terms: list[str]  # Terms that triggered flags
    summary: str

class ContentModerationState(TypedDict):
    # Input content
    content_id: str
    content_text: str
    content_type: Literal["post", "comment", "review", "image_caption", "video_description"]
    author_id: str
    author_history: dict | None  # Previous violations, account age, etc.

    # Classification result
    classification: ContentClassification | None

    # Analysis results
    toxicity_score: float | None
    spam_indicators: list[str] | None
    context_notes: str | None

    # Moderation decision
    action: Literal["approve", "reject", "flag_for_review", "quarantine"] | None
    moderator_notes: str | None

    # Human review
    review_decision: dict | None  # {approved: bool, action: str, notes: str}

    # Messages for logging
    messages: list[str] | None
