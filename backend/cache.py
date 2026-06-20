import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_cached_profile(username: str, role: str):
    try:
        result = supabase.table("profile_cache") \
            .select("*") \
            .eq("username", username) \
            .eq("role", role) \
            .execute()
        if result.data:
            print(f"Cache hit for {username} - {role}")
            return result.data[0].get("data")
        else:
            print(f"Cache miss for {username} - {role}")
            return None
    except Exception as e:
        print(f"Error checking cache: {e}")
        return None

def save_cached_profile(username: str, role: str, data: dict):
    try:
        result = supabase.table("profile_cache") \
            .upsert({
                "username": username,
                "role": role,
                "data": data,
                "last_commit": data.get("last_commit"),
                "updated_at": "now()"
            }) \
            .execute()
        print(f"Cached data for {username} - {role}")
        return result.data
    except Exception as e:
        print(f"Error saving cache: {e}")
        return None

def clear_cache(username: str = None, role: str = None):
    try:
        query = supabase.table("profile_cache")
        if username and role:
            query = query.delete().eq("username", username).eq("role", role)
        elif username:
            query = query.delete().eq("username", username)
        else:
            query = query.delete().neq("username", "nonexistent")
        query.execute()
        print(f"Cache cleared for {username or 'all'}")
    except Exception as e:
        print(f"Error clearing cache: {e}")