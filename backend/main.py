from fastapi import FastAPI, Query
from backend.github_service import get_cleaned_profile

app = FastAPI(title="GitReady API", description="GitHub profile analyzer")

@app.get("/analyze")
def analyze(username: str = Query(..., description="GitHub username"), role: str = Query("backend", description="Job role")):
    profile_data = get_cleaned_profile(username)
    
    return {
        "username": username,
        "role": role,
        "total_repos": len(profile_data),
        "repos": profile_data
    }