import sys
sys.path.append(".")

from backend.job_pipeline import fetch_job_postings

# Test with one role
skills = fetch_job_postings("frontend developer")

print("\n--- RESULT ---")
print(f"Total skill mentions: {len(skills)}")
print(f"Unique skills: {list(set(skills))}")