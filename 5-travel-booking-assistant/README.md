# Travel Booking Assistant

A LangGraph-based AI agent for automated travel booking with human-in-the-loop review for complex or high-value requests.

## Features

- **Intent Classification**: Identifies flight searches, hotel bookings, packages, cancellations, and modifications
- **Detail Extraction**: Automatically parses travel dates, destinations, budgets, and traveler count
- **Multi-Source Search**: Searches flights, hotels, or complete packages based on intent
- **Smart Routing**: Auto-books simple requests, escalates complex ones to human agents
- **Budget-Aware**: Considers user budget when presenting options and deciding review needs

## Architecture

```
START → parse_request → classify_intent
                                     ↓
                          ┌──────────┴──────────┐
                          ↓                     ↓
                  extract_details         human_agent → END
                          ↓
                    ┌─────┴─────┐
                    ↓           ↓
            search_flights   search_hotels
                    ↓           ↓
                    └─────┬─────┘
                          ↓
                  search_packages
                          ↓
                  present_options
                          ↓
                    ┌─────┴─────┐
                    ↓           ↓
              human_review   confirm_booking → END
                    ↓
              ┌─────┴─────┐
              ↓           ↓
   confirm_booking    END
```

## Workflow

1. **parse_request** - Logs incoming travel request
2. **classify_intent** - Determines intent type and complexity
3. **extract_details** - Parses dates, destinations, budget, travelers
4. **search_flights** - Queries flight APIs (simulated)
5. **search_hotels** - Queries hotel APIs (simulated)
6. **search_packages** - Queries package deals (simulated)
7. **present_options** - Selects best option based on budget
8. **human_review** - Pauses for agent approval on high-value bookings
9. **confirm_booking** - Processes payment and sends confirmation
10. **human_agent** - Escalates complex requests to human agents

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the assistant:
```bash
python main.py
```

## Test Cases

The `main.py` includes 5 scenarios:
- ✈️ Simple flight search (auto-book)
- 🏨 Luxury hotel request (human review)
- 📦 Package deal (auto-book)
- ❌ Cancellation request (escalate to agent)
- 💝 Complex honeymoon inquiry (escalate to agent)

## Customization

- Integrate real flight/hotel APIs (Amadeus, Sabre, Booking.com)
- Add payment processing in `confirm_booking`
- Implement email notifications
- Add multi-turn conversation support
- Include travel insurance options
- Add price tracking and alerts
