from fastapi import FastAPI, Query
from backend.github_service import get_cleaned_profile
from backend.analytics import log_analysis
from backend.skill_extractor import extract_skills
from backend.gap_analyzer import analyze_gaps
from backend.action_plan import generate_action_plan
from backend.skills_taxonomy import get_taxonomy_from_supabase

app = FastAPI(title="GitReady API", description="GitHub profile analyzer")

@app.get("/analyze")
def analyze(username: str = Query(..., description="GitHub username"), role: str = Query("backend", description="Job role")):
    profile_data = get_cleaned_profile(username)
    taxonomy_data = get_taxonomy_from_supabase(role)
    print("TAXONOMY DATA:", taxonomy_data)
    
    skill_result = extract_skills(profile_data, taxonomy_data)
    gap_result = analyze_gaps(skill_result, taxonomy_data)
    
    matched = skill_result.get("matched", [])
    missing = gap_result.get("gaps", [])
    score = gap_result.get("weighted_score", 75.0)
    
    action_plan = generate_action_plan(role, score, matched, missing)
    
    log_analysis(username, role, score, missing)
    
    return {
        "username": username,
        "role": role,
        "total_repos": len(profile_data),
        "score": score,
        "skill_gaps": missing,
        "action_plan": action_plan,
        "repos": profile_data
    }