from typing import Optional
import uuid
from supabase import Client
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

class UserService:
    def __init__(self, db: Client):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[dict]:
        try:
            response = self.db.table("users").select("*").eq("email", email).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None

    def create_user(self, user_in: UserCreate) -> Optional[dict]:
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user_in.password)
        
        user_data = {
            "id": user_id,
            "email": user_in.email,
            "full_name": user_in.full_name,
            "role": user_in.role,
            "hashed_password": hashed_password
        }
        
        try:
            response = self.db.table("users").insert(user_data).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
