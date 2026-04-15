"""
User-facing Agent with PostgreSQL Database Access
==================================================
This agent handles application users who want to:
1. Get customer information
2. Retrieve conversation history  
3. Analyze past conversations to fill out forms
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import json
from datetime import datetime

from src.agents.state import AgentState
from src.config import config
from src.db.models import Customer, Conversation, Message

llm = ChatOpenAI(model="gpt-4o-mini", api_key=config.OPENAI_API_KEY)

# Initialize memory checkpointer
memory = MemorySaver()

async def get_customer_from_db(contact_id: str, db_session) -> dict:
    """Fetch customer info from PostgreSQL."""
    result = await db_session.execute(
        select(Customer)
        .options(selectinload(Customer.conversations).selectinload(Conversation.messages))
        .where(Customer.chatwoot_contact_id == str(contact_id))
    )
    customer = result.scalars().first()
    if not customer:
        return None
    
    # Build customer data with conversations
    customer_data = {
        "contact_id": customer.chatwoot_contact_id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "extracted_data": customer.extracted_data or {},
        "created_at": str(customer.created_at),
        "conversations": []
    }
    
    for conv in customer.conversations:
        conv_data = {
            "conversation_id": conv.chatwoot_conversation_id,
            "status": conv.status,
            "created_at": str(conv.created_at),
            "messages": [
                {
                    "sender": msg.sender_type,
                    "content": msg.content,
                    "time": str(msg.created_at)
                }
                for msg in conv.messages
            ]
        }
        customer_data["conversations"].append(conv_data)
    
    return customer_data

async def call_model(state: AgentState, config: RunnableConfig):
    """
    Main node for the agent. Handles context retrieval and LLM interaction.
    """
    db_session = config["configurable"].get("db_session")
    
    # 1. Try to find contact_id in the latest message
    latest_message = state["messages"][-1].content
    contact_id = None
    
    for word in latest_message.lower().split():
        if word.isdigit():
            contact_id = word
            break
            
    # 2. If not found in current message, check if we have one in state
    if not contact_id and state.get("customer_info"):
        contact_id = state["customer_info"].get("contact_id")
    
    customer_context = ""
    customer_found = False
    
    # 3. If we have a contact_id, fetch/refresh data
    if contact_id:
        customer_data = await get_customer_from_db(contact_id, db_session)
        if customer_data:
            customer_found = True
            customer_context = f"""
CUSTOMER DATA (Contact ID: {contact_id}):
- Name: {customer_data['name'] or 'Not provided'}
- Email: {customer_data['email'] or 'Not provided'}
- Phone: {customer_data['phone'] or 'Not provided'}
- Created: {customer_data['created_at']}

CONVERSATION HISTORY:
"""
            for conv in customer_data['conversations']:
                customer_context += f"\n--- Conversation {conv['conversation_id']} ({conv['created_at']}) ---\n"
                for msg in conv['messages'][:20]:
                    customer_context += f"[{msg['sender']}] {msg['content']}\n"
            
            # Update state with the found context/ID
            state["customer_info"] = {
                "contact_id": contact_id,
                "has_data": True
            }

    # 4. Prepare system prompt
    system_prompt = f"""You are a customer data assistant for application users.

You help users analyze customer data and conversation history.

{customer_context}

If customer data is provided above, use it to answer the user's questions.
If the user asks about a customer and you don't have their data (either above or in context), ask for the contact_id.
Present information in a clear, organized format.
Be professional and concise."""

    # 5. Invoke LLM with System prompt + History (state['messages'])
    # We prepend the system prompt to the messages list
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = await llm.ainvoke(messages)
    
    return {
        "messages": [response],
        "customer_info": state.get("customer_info", {})
    }

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# Compile with memory checkpointer
app = workflow.compile(checkpointer=memory)

async def run_user_agent(user_id: str, message: str, db_session) -> dict:
    """
    Entry point to run the agent with persistence.
    """
    config = {"configurable": {"thread_id": user_id, "db_session": db_session}}
    
    # Run the graph
    # add_messages will append the new HumanMessage to the existing state
    inputs = {"messages": [HumanMessage(content=message)]}
    result = await app.ainvoke(inputs, config)
    
    # Get the last message and the context state
    last_msg = result["messages"][-1]
    has_context = result.get("customer_info", {}).get("has_data", False)
    
    return {
        "response": last_msg.content,
        "customer_context": "Found" if has_context else None
    }
