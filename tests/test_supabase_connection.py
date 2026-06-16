# create a new file tests/test_supabase_connection.py
import sys
sys.path.append(".")

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"URL: {SUPABASE_URL}")
print(f"KEY starts with: {SUPABASE_KEY[:20] if SUPABASE_KEY else 'NONE'}...")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Try a simple insert
try:
    result = supabase.table("taxonomy").insert({
        "role": "test role",
        "skills": {"test_skill": 1.0}
    }).execute()
    print("SUCCESS:", result.data)
except Exception as e:
    print("ERROR:", e)