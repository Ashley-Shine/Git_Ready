from fastapi import FastAPI, Query
from backend.github_service import get_cleaned_profile
from backend.analytics import log_analysis

app = FastAPI(title="GitReady API", description="GitHub profile analyzer")

@app.get("/analyze")
def analyze(username: str = Query(..., description="GitHub username"), role: str = Query("backend", description="Job role")):
    profile_data = get_cleaned_profile(username)
    score = 75
    skill_gaps = ["FastAPI", "PostgreSQL", "Docker"]      # Person 2
    
    log_analysis(username, role, score, skill_gaps)
    return {
        "username": username,
        "role": role,
        "total_repos": len(profile_data),
        "repos": profile_data
    }