from supabase import create_client, Client
from app.core.config import settings

def get_supabase() -> Client:
    # Initialize the Supabase client
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        # Prevent failure during initial startup without env variables
        print("Warning: SUPABASE_URL or SUPABASE_KEY is missing. Database operations will fail.")
        return None
    
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return supabase

supabase_client = get_supabase()
