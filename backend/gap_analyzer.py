def analyze_gaps(skill_match_result: dict, taxonomy: dict) -> dict:
    """
    Takes output from extract_skills and produces:
    - skill match percentage
    - weighted score (accounts for importance of missing skills)
    - ranked gap list for action plan
    """
    matched = skill_match_result["matched"]
    missing = skill_match_result["missing"]

    total_skills = len(matched) + len(missing)
    if total_skills == 0:
        return {"match_percentage": 0, "weighted_score": 0, "gaps": []}

    
    match_percentage = round((len(matched) / total_skills) * 100, 1)

    
    total_weight = sum(taxonomy["skills"].values())
    missing_weight = sum(s["importance"] for s in missing)
    weighted_score = round(((total_weight - missing_weight) / total_weight) * 100, 1)

    return {
        "match_percentage": match_percentage,
        "weighted_score": weighted_score,
        "gaps": missing 
    }


if __name__ == "__main__":
    from sys import path
    path.append(".")
    from shared.schemas import SAMPLE_CLEANED_REPO, SAMPLE_TAXONOMY
    from backend.skill_extractor import extract_skills

    skill_result = extract_skills([SAMPLE_CLEANED_REPO], SAMPLE_TAXONOMY)
    gap_result = analyze_gaps(skill_result, SAMPLE_TAXONOMY)

    print("Match percentage:", gap_result["match_percentage"], "%")
    print("Weighted score:", gap_result["weighted_score"], "%")
    print("Gaps to fix:")
    for g in gap_result["gaps"]:
        print(f"  {g['skill']} (importance: {g['importance']})")