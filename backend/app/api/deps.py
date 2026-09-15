from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from supabase import Client

from app.core.config import settings
from app.core import security
from app.schemas.user import TokenPayload, User
from app.db.database import supabase_client

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_db() -> Client:
    if not supabase_client:
        raise HTTPException(status_code=500, detail="Database connection not configured")
    return supabase_client

def get_current_user(
    db: Client = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Query user from Supabase using user_id in sub
    response = db.table("users").select("*").eq("id", token_data.sub).execute()
    
    if not response.data or len(response.data) == 0:
        raise HTTPException(status_code=404, detail="User not found")
        
    user_data = response.data[0]
    return User(**user_data)

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    # In a real app, you might have an 'is_active' flag
    return current_user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
