import os
from dotenv import load_dotenv
from groq import Groq
from backend.prompts import ACTION_PLAN_PROMPT

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_action_plan(role: str, score: float, matched: list, missing: list) -> str:
    matched_skills = ", ".join([m["skill"] for m in matched]) or "None yet"
    missing_skills = ", ".join([f"{m['skill']} (importance: {m['importance']})" for m in missing])

    prompt = ACTION_PLAN_PROMPT.format(
        role=role,
        score=score,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    from sys import path
    path.append(".")
    from shared.schemas import SAMPLE_CLEANED_REPO, SAMPLE_TAXONOMY
    from backend.skill_extractor import extract_skills
    from backend.gap_analyzer import analyze_gaps

    skill_result = extract_skills([SAMPLE_CLEANED_REPO], SAMPLE_TAXONOMY)
    gap_result = analyze_gaps(skill_result, SAMPLE_TAXONOMY)

    plan = generate_action_plan(
        role=SAMPLE_TAXONOMY["role"],
        score=gap_result["weighted_score"],
        matched=skill_result["matched"],
        missing=gap_result["gaps"]
    )

    print(plan)