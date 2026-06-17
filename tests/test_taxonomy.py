import sys
sys.path.append(".")

from backend.job_pipeline import fetch_job_postings
from backend.skills_taxonomy import build_taxonomy_with_embeddings, get_taxonomy_from_supabase

# Step 1 - Get raw skills from Day 2 pipeline
raw_skills = fetch_job_postings("frontend developer")

# Step 2 - Build taxonomy using embeddings
taxonomy = build_taxonomy_with_embeddings("frontend developer", raw_skills)

# Step 3 - Verify it was saved and can be retrieved
print("\n--- Fetching from Supabase ---")
saved = get_taxonomy_from_supabase("frontend developer")
print(saved)



from backend.skills_taxonomy import get_taxonomy_from_supabase

print("\n--- Checking Supabase ---")
result = get_taxonomy_from_supabase("frontend developer")

if result:
    print("✅ Data found in Supabase!")
    print(f"Role: {result['role']}")
    print(f"Skills: {result['skills']}")
else:
    print("❌ No data found in Supabase")