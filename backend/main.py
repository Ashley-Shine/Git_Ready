from fastapi import FastAPI, Query
from backend.github_service import get_cleaned_profile
from backend.analytics import log_analysis
from backend.quality_scorer import score_repo_quality, calculate_final_score

app = FastAPI(title="GitReady API", description="GitHub profile analyzer")

@app.get("/analyze")
def analyze(
    username: str = Query(..., description="GitHub username"),
    role: str = Query("backend", description="Job role")
):
    # Person 1 → repo data
    profile_data = get_cleaned_profile(username)

    # Person 2 → skill match and gaps
    score = 75
    skill_gaps = ["FastAPI", "PostgreSQL", "Docker"]

    # Person 3 → quality scoring
    repo_quality = score_repo_quality(profile_data)
    final_score = calculate_final_score(score, repo_quality)

    # Log analysis
    log_analysis(username, role, score, skill_gaps)

    # ✅ Return JSON response
    return {
        "username": username,
        "role": role,
        "total_repos": len(profile_data),
        "repos": profile_data,
        "skill_gaps": skill_gaps,
        "quality_score": repo_quality,
        "final_score": final_score
    }
