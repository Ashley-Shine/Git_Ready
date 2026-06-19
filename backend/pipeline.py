from backend.skill_extractor import extract_skills
from backend.gap_analyzer import analyze_gaps
from backend.action_plan import generate_action_plan
from backend.skills_taxonomy import get_taxonomy_from_supabase
from backend.github_service import get_cleaned_profile

def run_ai_pipeline(cleaned_repos: list, role: str) -> dict:
   
    taxonomy = get_taxonomy_from_supabase(role)

    if not taxonomy or "skills" not in taxonomy:
        return {"error": f"No taxonomy found for role: {role}"}

    skill_result = extract_skills(cleaned_repos, taxonomy)
    gap_result = analyze_gaps(skill_result, taxonomy)

    plan = generate_action_plan(
        role=taxonomy["role"],
        score=gap_result["weighted_score"],
        matched=skill_result["matched"],
        missing=gap_result["gaps"]
    )

    return {
        "skill_match_pct": gap_result["match_percentage"],
        "weighted_score": gap_result["weighted_score"],
        "matched_skills": skill_result["matched"],
        "skill_gaps": gap_result["gaps"],
        "action_plan": plan
    }


if __name__ == "__main__":

    cleaned_repos = get_cleaned_profile("octocat")
    result = run_ai_pipeline(cleaned_repos, role="frontend developer")
    print(result)