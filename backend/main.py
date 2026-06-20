from fastapi import FastAPI, Query
from backend.github_service import get_cleaned_profile
from backend.analytics import log_analysis
from backend.skill_extractor import extract_skills
from backend.gap_analyzer import analyze_gaps
from backend.action_plan import generate_action_plan
from backend.skills_taxonomy import get_taxonomy_from_supabase
from backend.quality_scorer import score_repo_quality, calculate_final_score
from backend.cache import get_cached_profile, save_cached_profile
from backend.github_service import get_cleaned_profile, get_last_push_date

app = FastAPI(title="GitReady API", description="GitHub profile analyzer")

@app.get("/analyze")
def analyze(username: str = Query(..., description="GitHub username"), role: str = Query("backend", description="Job role")):
    last_commit = get_last_push_date(username)
    cached_data = get_cached_profile(username, role)
    if cached_data:
        cached_commit = cached_data.get("last_commit")
        print(f"DEBUG: last_commit = {last_commit}")
        print(f"DEBUG: cached_commit = {cached_commit}")
        if last_commit and cached_commit and last_commit == cached_commit:
            print("DEBUG: Cache valid, returning cached")
            return cached_data
        else:
            print("DEBUG: Cache stale or missing commit info")
    #if not found in cache:         
    profile_data = get_cleaned_profile(username)
    taxonomy_data = get_taxonomy_from_supabase(role)
    print("TAXONOMY DATA:", taxonomy_data)
    
    skill_result = extract_skills(profile_data, taxonomy_data)
    print("SKILL RESULT:", skill_result)
    print("MISSING TYPE:", type(skill_result.get("missing", [])))
    print("MISSING CONTENT:", skill_result.get("missing", []))
    gap_result = analyze_gaps(skill_result, taxonomy_data)
    
    matched = skill_result.get("matched", [])
    missing = gap_result.get("gaps", [])

    skill_score = gap_result.get("weighted_score", 75.0)    
    
    total_quality = 0
    for repo in profile_data:
        total_quality += score_repo_quality(repo)
    quality_score = total_quality /len(profile_data) if profile_data else 0
    final_score = calculate_final_score(skill_score, quality_score)

    action_plan = generate_action_plan(role, final_score, matched, missing)

    log_analysis(username, role, final_score, missing)
    
    result= {
        "username": username,
        "role": role,
        "total_repos": len(profile_data),
        "score": final_score,
        "skill_score":skill_score,
        "skill_match_pct": skill_score,
        "quality_score":quality_score,
        "skill_gaps": missing,
        "action_plan": action_plan,
        "repos": [
        {
            **repo,
            "language": ", ".join(repo.get("tech_stack", [])) if repo.get("tech_stack") else None
        }
        for repo in profile_data
        ],
        "last_commit": last_commit
    }
    save_cached_profile(username, role, result)
    return result