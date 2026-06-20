from backend.skill_extractor import extract_skills


def test_extract_skills_normal_case():
    """User has some matching skills and some missing ones."""
    repo = {"tech_stack": ["Python", "FastAPI"]}
    taxonomy = {"role": "backend", "skills": {"python": 0.9, "fastapi": 0.8, "docker": 0.5}}

    result = extract_skills([repo], taxonomy)

    assert len(result["matched"]) == 2
    assert len(result["missing"]) == 1
    assert result["missing"][0]["skill"] == "docker"


def test_extract_skills_empty_tech_stack():
    """
    Regression test for the bug found during integration testing:
    when tech_stack is empty, 'missing' must still be a list of dicts
    (not a list of plain strings), so downstream code in gap_analyzer.py
    doesn't crash on s["importance"].
    """
    repo = {"tech_stack": []}
    taxonomy = {"role": "backend", "skills": {"python": 0.9, "fastapi": 0.8}}

    result = extract_skills([repo], taxonomy)

    assert result["matched"] == []
    assert len(result["missing"]) == 2
    assert all(isinstance(item, dict) for item in result["missing"])
    assert all("skill" in item and "importance" in item for item in result["missing"])


def test_extract_skills_no_repos():
    """No repos at all should behave the same as empty tech_stack."""
    taxonomy = {"role": "backend", "skills": {"python": 0.9}}

    result = extract_skills([], taxonomy)

    assert result["matched"] == []
    assert all(isinstance(item, dict) for item in result["missing"])