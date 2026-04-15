from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from src.db.session import get_db
from src.db.models import User
from src.core.auth import get_current_active_admin
from src.core.security import get_password_hash
from src.schemas.user import UserCreate, User as UserSchema

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserSchema)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """
    Admin can add more users.
    """
    # Check if username/email already exists
    result = await db.execute(select(User).where((User.username == user_in.username) | (User.email == user_in.email)))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserSchema])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """
    Admin can view all users.
    """
    result = await db.execute(select(User))
    return result.scalars().all()
