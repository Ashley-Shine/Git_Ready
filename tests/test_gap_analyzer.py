from backend.gap_analyzer import analyze_gaps


def test_analyze_gaps_normal_case():
    """Mix of matched and missing skills produces correct percentages."""
    skill_result = {
        "matched": [
            {"skill": "python", "matched_by": "Python", "importance": 0.9},
            {"skill": "fastapi", "matched_by": "FastAPI", "importance": 0.8}
        ],
        "missing": [
            {"skill": "docker", "importance": 0.5}
        ]
    }
    taxonomy = {"role": "backend", "skills": {"python": 0.9, "fastapi": 0.8, "docker": 0.5}}

    result = analyze_gaps(skill_result, taxonomy)

    assert result["match_percentage"] == round((2 / 3) * 100, 1)
    assert result["gaps"] == skill_result["missing"]
    assert "weighted_score" in result


def test_analyze_gaps_all_matched():
    """User has every required skill — should score 100% on both metrics."""
    skill_result = {
        "matched": [
            {"skill": "python", "matched_by": "Python", "importance": 0.9}
        ],
        "missing": []
    }
    taxonomy = {"role": "backend", "skills": {"python": 0.9}}

    result = analyze_gaps(skill_result, taxonomy)

    assert result["match_percentage"] == 100.0
    assert result["weighted_score"] == 100.0
    assert result["gaps"] == []


def test_analyze_gaps_none_matched():
    """User has none of the required skills — should score 0% match."""
    skill_result = {
        "matched": [],
        "missing": [
            {"skill": "python", "importance": 0.9},
            {"skill": "fastapi", "importance": 0.8}
        ]
    }
    taxonomy = {"role": "backend", "skills": {"python": 0.9, "fastapi": 0.8}}

    result = analyze_gaps(skill_result, taxonomy)

    assert result["match_percentage"] == 0.0
    assert result["weighted_score"] == 0.0


def test_analyze_gaps_empty_skill_result():
    """No skills at all (matched or missing) shouldn't crash — should return zeros."""
    skill_result = {"matched": [], "missing": []}
    taxonomy = {"role": "backend", "skills": {"python": 0.9}}

    result = analyze_gaps(skill_result, taxonomy)

    assert result == {"match_percentage": 0, "weighted_score": 0, "gaps": []}