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
    
    # Step 1 — Check cache first (instant return if valid)
    last_commit = get_last_push_date(username)
    cached_data = get_cached_profile(username, role_lower)
    if cached_data:
        cached_commit = cached_data.get("last_commit")
        if last_commit and cached_commit and last_commit == cached_commit:
            print(f"Cache hit for {username} - {role_lower}")
            return cached_data
        else:
            print(f"Cache stale for {username} - {role_lower}")

    # Step 2 — Fetch GitHub profile (limited to 10 repos)
    print(f"Fetching profile for {username}...")
    profile_data = get_cleaned_profile(username)
    profile_data = profile_data[:10]  # limit to 10 repos for speed
    print(f"Processing {len(profile_data)} repos")

    # Step 3 — Get taxonomy from Supabase (build from Adzuna only if missing)
    taxonomy_data = get_taxonomy_from_supabase(role_lower)
    if not taxonomy_data or "skills" not in taxonomy_data:
        print(f"No taxonomy found for '{role_lower}', building from Adzuna...")
        raw_skills = fetch_job_postings(role_lower)
        taxonomy_data = build_taxonomy_with_embeddings(role_lower, raw_skills)

    # Step 4 — Skill extraction and gap analysis
    skill_result = extract_skills(profile_data, taxonomy_data)
    gap_result = analyze_gaps(skill_result, taxonomy_data)

    matched = skill_result.get("matched", [])
    missing = gap_result.get("gaps", [])
    skill_score = gap_result.get("weighted_score", 75.0)

    # Step 5 — Quality scoring (calculated once per repo, reused)
    repos_with_quality = []
    total_quality = 0
    for repo in profile_data:
        q = score_repo_quality(repo)
        total_quality += q
        repos_with_quality.append({
            **repo,
            "language": ", ".join(repo.get("tech_stack", [])) if repo.get("tech_stack") else None,
            "quality_score": q
        })
    quality_score = total_quality / len(profile_data) if profile_data else 0

    # Step 6 — Final score
    final_score = calculate_final_score(skill_score, quality_score)

    print(f"skill_score: {skill_score}")
    print(f"quality_score: {quality_score}")
    print(f"final_score: {final_score}")

    # Step 7 — Action plan and logging
    action_plan = generate_action_plan(role_lower, final_score, matched, missing)
    log_analysis(username, role_lower, final_score, missing)

    # Step 8 — Analytics (from Supabase logs)
    analytics_data = {
        "trending_gaps": get_trending_gaps(role_lower),
        "average_score": get_average_score(role_lower)
    }

    # Step 9 — Job data from taxonomy (no extra Adzuna call)
    job_data = list(taxonomy_data.get("skills", {}).keys()) if taxonomy_data else []

    # Step 10 — Build and cache result
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
        "repos": repos_with_quality,
        "last_commit": last_commit
    }

    save_cached_profile(username, role_lower, result)
    print(f"Analysis complete for {username} - {role_lower}")
    return result


@app.get("/refresh-taxonomy")
def refresh_taxonomy_endpoint(role: str = Query(..., description="Job role to refresh")):
    """
    Fetches live job data from Adzuna and rebuilds the taxonomy for a role.
    """
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