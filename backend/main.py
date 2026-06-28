from fastapi import FastAPI, Query
from backend.github_service import get_cleaned_profile, get_last_push_date
from backend.analytics import log_analysis, get_trending_gaps, get_average_score
from backend.skill_extractor import extract_skills
from backend.gap_analyzer import analyze_gaps
from backend.action_plan import generate_action_plan
from backend.skills_taxonomy import get_taxonomy_from_supabase, build_taxonomy_with_embeddings
from backend.quality_scorer import score_repo_quality, calculate_final_score
from backend.cache import get_cached_profile, save_cached_profile
from backend.job_pipeline import fetch_job_postings

app = FastAPI(title="GitReady API", description="GitHub profile analyzer")

@app.get("/analyze")
def analyze(username: str = Query(..., description="GitHub username"), role: str = Query("backend", description="Job role")):
    
    role_lower = role.lower().strip()
    
    last_commit = get_last_push_date(username)
    cached_data = get_cached_profile(username, role_lower)
    if cached_data:
        cached_commit = cached_data.get("last_commit")
        print(f"DEBUG: last_commit = {last_commit}")
        print(f"DEBUG: cached_commit = {cached_commit}")
        if last_commit and cached_commit and last_commit == cached_commit:
            print("DEBUG: Cache valid, returning cached")
            return cached_data
        else:
            print("DEBUG: Cache stale or missing commit info")

    profile_data = get_cleaned_profile(username)

    taxonomy_data = get_taxonomy_from_supabase(role_lower)
    if not taxonomy_data or "skills" not in taxonomy_data:
        print(f"No taxonomy found for '{role}', building live from Adzuna...")
        raw_skills = fetch_job_postings(role)
        taxonomy_data = build_taxonomy_with_embeddings(role, raw_skills)

    print("TAXONOMY DATA:", taxonomy_data)

    skill_result = extract_skills(profile_data, taxonomy_data)
    print("SKILL RESULT:", skill_result)
    print("MISSING TYPE:", type(skill_result.get("missing", [])))
    print("MISSING CONTENT:", skill_result.get("missing", []))
    
    gap_result = analyze_gaps(skill_result, taxonomy_data)

    matched = skill_result.get("matched", [])
    missing = gap_result.get("gaps", [])
    skill_score = gap_result.get("weighted_score", 75.0)

    # Add quality_score and language to each repo
    total_quality = 0
    for repo in profile_data:
        q = score_repo_quality(repo)
        total_quality += q
        repo["quality_score"] = q
        repo["language"] = ", ".join(repo.get("tech_stack", [])) if repo.get("tech_stack") else None

    quality_score = total_quality / len(profile_data) if profile_data else 0
    final_score = calculate_final_score(skill_score, quality_score)

    action_plan = generate_action_plan(role_lower, final_score, matched, missing)

    log_analysis(username, role_lower, final_score, missing)

    analytics_data = {
        "trending_gaps": get_trending_gaps(role_lower),
        "average_score": get_average_score(role_lower)
    }

    job_data = list(taxonomy_data.get("skills", {}).keys()) if taxonomy_data else []

    result = {
        "username": username,
        "role": role_lower,
        "total_repos": len(profile_data),
        "score": final_score,
        "final_score": final_score,
        "skill_score": skill_score,
        "skill_match_pct": skill_score,
        "quality_score": quality_score,
        "skill_gaps": missing,
        "action_plan": action_plan,
        "analytics": analytics_data,
        "job_data": job_data,
        "taxonomy": taxonomy_data,
        "repos": profile_data,
        "last_commit": last_commit
    }

    save_cached_profile(username, role_lower, result)
    return result


@app.get("/refresh-taxonomy")
def refresh_taxonomy_endpoint(role: str = Query(..., description="Job role to refresh")):
    role_lower = role.lower().strip()
    print(f"Refreshing taxonomy for '{role_lower}' from live Adzuna data...")
    
    raw_skills = fetch_job_postings(role_lower)
    
    if not raw_skills:
        return {"status": "error", "message": f"No skills found for {role_lower}"}
    
    taxonomy = build_taxonomy_with_embeddings(role_lower, raw_skills)
    
    return {
        "status": "success",
        "role": role_lower,
        "skills_count": len(taxonomy.get("skills", {})),
        "skills": taxonomy.get("skills", {})
    }