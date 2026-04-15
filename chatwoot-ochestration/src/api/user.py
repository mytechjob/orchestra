from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.db.models import User
from src.core.auth import get_current_user
from src.agents.user_graph import run_user_agent
from src.schemas.user import ChatMessage

router = APIRouter()

@router.post("/api/user/chat")
async def user_chat(
    chat_in: ChatMessage, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Conversational API for application users to interact with customer data.
    
    Users can:
    - Ask about customer information: "Tell me about customer 123"
    - Get conversation history: "Show me conversations for customer 123"
    - Extract form data: "Fill out a form for customer 123, I need name, email, phone"
    
    Args:
        message: User's natural language query
        db: Database session
    """
    try:
        result = await run_user_agent(str(current_user.id), chat_in.message, db)
        return {
            "user_id": current_user.id,
            "response": result["response"],
            "customer_provided": result["customer_context"] is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
