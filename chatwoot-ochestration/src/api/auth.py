from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Keep it if you want to support both or remove if strictly JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.db.session import get_db
from src.db.models import User
from src.core.auth import get_current_user
from src.core.security import get_password_hash, verify_password, create_access_token
from src.schemas.user import UserCreate, User as UserSchema, Token, UserLogin

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserSchema)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if any user exists
    result = await db.execute(select(func.count(User.id)))
    count = result.scalar()
    
    if count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Registration is disabled. Please contact the administrator."
        )
    
    # Create the first user as Admin
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role="admin"
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user_in.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
