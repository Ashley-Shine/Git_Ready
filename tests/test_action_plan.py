from backend.action_plan import generate_action_plan


def test_generate_action_plan_returns_text():
    """
    Confirms the Groq connection works and returns usable text.
    """
    matched = [{"skill": "python", "matched_by": "Python", "importance": 0.9}]
    missing = [{"skill": "docker", "importance": 0.6}]

    plan = generate_action_plan(
        role="backend developer",
        score=65.0,
        matched=matched,
        missing=missing
    )

    assert isinstance(plan, str)
    assert len(plan) > 0
    assert "Day 1" in plan