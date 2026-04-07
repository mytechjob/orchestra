from typing import TypedDict, Literal

class TravelClassification(TypedDict):
    intent: Literal["flight_search", "hotel_search", "package", "cancellation", "modification", "general_inquiry"]
    complexity: Literal["simple", "moderate", "complex"]
    budget_range: Literal["budget", "mid_range", "luxury", "premium"]
    urgency: Literal["low", "medium", "high"]
    summary: str

class TravelBookingState(TypedDict):
    # User input
    user_id: str
    request_text: str
    conversation_history: list[str] | None

    # Classification
    classification: TravelClassification | None

    # Travel details extracted
    origin: str | None
    destination: str | None
    check_in: str | None
    check_out: str | None
    travelers: int | None
    budget: float | None

    # Search results
    flight_options: list[dict] | None
    hotel_options: list[dict] | None
    package_options: list[dict] | None

    # Booking details
    selected_option: dict | None
    booking_confirmation: dict | None
    total_price: float | None

    # Human review
    review_decision: dict | None

    # Messages
    messages: list[str] | None
