from typing import Literal
from langgraph.graph import END
from langgraph.types import interrupt, Command
from langchain.messages import HumanMessage
from states import TravelBookingState, TravelClassification
from llm import llm

def parse_request(state: TravelBookingState) -> dict:
    """Log and initialize user request"""
    return {
        "messages": [HumanMessage(content=f"Processing travel request: {state['request_text'][:100]}")]
    }

def classify_intent(state: TravelBookingState) -> Command[Literal["extract_details", "human_agent"]]:
    """Classify user intent and determine complexity"""

    structured_llm = llm.with_structured_output(TravelClassification)

    classification_prompt = f"""
    Analyze this travel request:

    User Request: {state['request_text']}

    Classify the intent (flight_search, hotel_search, package, cancellation, modification, general_inquiry),
    complexity level, budget range, and urgency.
    """

    classification = structured_llm.invoke(classification_prompt)

    # Route complex requests, cancellations, or modifications to human agent
    if classification['complexity'] == 'complex' or classification['intent'] in ['cancellation', 'modification']:
        goto = "human_agent"
    else:
        goto = "extract_details"

    return Command(
        update={"classification": classification},
        goto=goto
    )

def extract_details(state: TravelBookingState) -> Command[Literal["search_flights", "search_hotels", "search_packages"]]:
    """Extract travel details from user request using LLM"""

    classification = state.get('classification', {})

    extraction_prompt = f"""
    Extract travel details from this request:

    Request: {state['request_text']}
    Intent: {classification.get('intent', 'unknown')}

    Return a JSON with these fields (use null if not provided):
    - origin: departure city/airport
    - destination: arrival city/airport
    - check_in: travel start date or hotel check-in
    - check_out: travel end date or hotel check-out
    - travelers: number of travelers
    - budget: estimated budget in USD
    """

    response = llm.invoke(extraction_prompt)

    # Parse extracted details (in production, use structured output)
    # Placeholder parsing - would use JSON parsing in real implementation
    extracted = {
        "origin": "New York",
        "destination": "Los Angeles",
        "check_in": "2026-05-01",
        "check_out": "2026-05-05",
        "travelers": 2,
        "budget": 1500.0
    }

    # Determine next node based on intent
    intent = classification.get('intent', 'general_inquiry')
    if intent == 'flight_search':
        goto = "search_flights"
    elif intent == 'hotel_search':
        goto = "search_hotels"
    else:
        goto = "search_packages"

    return Command(
        update=extracted,
        goto=goto
    )

def search_flights(state: TravelBookingState) -> Command[Literal["present_options"]]:
    """Search for flight options (simulated)"""

    print(f"🔍 Searching flights: {state.get('origin')} → {state.get('destination')}")

    # Simulated flight search results
    flight_options = [
        {
            "id": "FL001",
            "airline": "SkyWings",
            "departure": "08:00 AM",
            "arrival": "11:30 AM",
            "price": 350,
            "stops": 0
        },
        {
            "id": "FL002",
            "airline": "AirExpress",
            "departure": "02:00 PM",
            "arrival": "06:45 PM",
            "price": 280,
            "stops": 1
        },
        {
            "id": "FL003",
            "airline": "BudgetAir",
            "departure": "06:00 AM",
            "arrival": "10:15 AM",
            "price": 220,
            "stops": 1
        }
    ]

    return Command(
        update={"flight_options": flight_options},
        goto="present_options"
    )

def search_hotels(state: TravelBookingState) -> Command[Literal["present_options"]]:
    """Search for hotel options (simulated)"""

    print(f"🔍 Searching hotels in {state.get('destination')}")

    # Simulated hotel search results
    hotel_options = [
        {
            "id": "HT001",
            "name": "Grand Plaza Hotel",
            "rating": 4.5,
            "price_per_night": 180,
            "amenities": ["WiFi", "Pool", "Gym", "Restaurant"]
        },
        {
            "id": "HT002",
            "name": "Budget Inn",
            "rating": 3.5,
            "price_per_night": 95,
            "amenities": ["WiFi", "Breakfast"]
        },
        {
            "id": "HT003",
            "name": "Luxury Suites",
            "rating": 5.0,
            "price_per_night": 350,
            "amenities": ["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar"]
        }
    ]

    return Command(
        update={"hotel_options": hotel_options},
        goto="present_options"
    )

def search_packages(state: TravelBookingState) -> Command[Literal["present_options"]]:
    """Search for travel packages (flights + hotels)"""

    print(f"🔍 Searching travel packages: {state.get('origin')} → {state.get('destination')}")

    # Simulated package results
    package_options = [
        {
            "id": "PKG001",
            "description": "Standard Package",
            "flights": "SkyWings - Direct",
            "hotel": "Grand Plaza Hotel",
            "total_price": 1200,
            "includes": ["Flights", "Hotel", "Breakfast"]
        },
        {
            "id": "PKG002",
            "description": "Budget Package",
            "flights": "BudgetAir - 1 Stop",
            "hotel": "Budget Inn",
            "total_price": 750,
            "includes": ["Flights", "Hotel"]
        },
        {
            "id": "PKG003",
            "description": "Premium Package",
            "flights": "SkyWings - Direct",
            "hotel": "Luxury Suites",
            "total_price": 2400,
            "includes": ["Flights", "Hotel", "Breakfast", "Airport Transfer", "Spa Access"]
        }
    ]

    return Command(
        update={"package_options": package_options},
        goto="present_options"
    )

def present_options(state: TravelBookingState) -> Command[Literal["human_review", "confirm_booking"]]:
    """Present travel options to user and wait for selection"""

    classification = state.get('classification', {})
    
    # Build summary of available options
    summary = ""
    if state.get('flight_options'):
        summary += f"\nFlights found: {len(state['flight_options'])} options"
    if state.get('hotel_options'):
        summary += f"\nHotels found: {len(state['hotel_options'])} options"
    if state.get('package_options'):
        summary += f"\nPackages found: {len(state['package_options'])} options"

    # Select best option based on budget (simulated)
    if state.get('package_options'):
        selected = state['package_options'][0]  # Default to first option
    elif state.get('flight_options'):
        selected = state['flight_options'][0]
    else:
        selected = state.get('hotel_options', [{}])[0] if state.get('hotel_options') else {}

    # High-budget or complex requests need human review
    needs_review = (
        classification.get('budget_range') in ['luxury', 'premium'] or
        state.get('budget', 0) > 2000
    )

    return Command(
        update={
            "selected_option": selected,
            "total_price": selected.get('total_price', selected.get('price', 0))
        },
        goto="human_review" if needs_review else "confirm_booking"
    )

def human_review(state: TravelBookingState) -> Command[Literal["confirm_booking", END]]:
    """Pause for travel agent review on complex or high-value bookings"""

    review_data = interrupt({
        "user_id": state.get('user_id', ''),
        "request": state.get('request_text', ''),
        "selected_option": state.get('selected_option', {}),
        "total_price": state.get('total_price', 0),
        "classification": state.get('classification', {}),
        "action": "Please review this booking before confirmation"
    })

    if review_data.get('approved', True):
        goto = "confirm_booking"
    else:
        # Agent will handle manually
        goto = END

    return Command(
        update={"review_decision": review_data},
        goto=goto
    )

def confirm_booking(state: TravelBookingState) -> dict:
    """Confirm and process the booking"""
    
    selected = state.get('selected_option', {})
    print(f"✅ Booking confirmed: {selected.get('id', 'N/A')}")
    print(f"💰 Total price: ${state.get('total_price', 0):.2f}")
    print(f"📧 Confirmation sent to user {state.get('user_id')}")

    # Simulated booking confirmation
    booking_confirmation = {
        "booking_id": f"BK{state['user_id']}12345",
        "status": "confirmed",
        "total_paid": state.get('total_price', 0)
    }

    return {
        "booking_confirmation": booking_confirmation,
        "action": "booking_confirmed"
    }

def human_agent(state: TravelBookingState) -> dict:
    """Escalate to human travel agent for complex requests"""
    print(f"⚠️  Request escalated to human agent")
    print(f"📝 Request: {state['request_text']}")
    print(f"👤 User: {state.get('user_id')}")
    
    return {"action": "escalated_to_agent"}
