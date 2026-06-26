from typing import Dict, Any
from sentence_transformers import SentenceTransformer, util

# Load embeddings model once (you can swap for a lighter one if needed)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Reference set of "good README" examples (can expand later)
REFERENCE_READMES = [
    "This project includes clear installation steps, usage examples, and contribution guidelines.",
    "The repository provides a well-structured README with badges, CI status, and license information.",
    "Documentation covers purpose, tech stack, and links to further resources."
]
REFERENCE_EMBEDDINGS = model.encode(REFERENCE_READMES, convert_to_tensor=True)


def score_readme_quality_semantic(readme_text: str) -> float:
    """
    Compare README text against reference embeddings to get semantic similarity score.
    Returns a float between 0 and 1.
    """
    if not readme_text:
        return 0.0
    readme_embedding = model.encode(readme_text, convert_to_tensor=True)
    similarity = util.cos_sim(readme_embedding, REFERENCE_EMBEDDINGS).max().item()
    return round(similarity, 3)


def check_structural_quality(repo: Dict[str, Any]) -> float:
    """
    Rule-based structural checks: tests, CI, license.
    Returns a score between 0 and 1.
    """
    score = 0
    checks = ["has_tests", "has_ci", "license"]
    for check in checks:
        if repo.get(check):
            score += 1
    return score / len(checks)


def score_repo_quality(repo: Dict[str, Any]) -> int:
    """
    Combine semantic and structural scores into a 0–100 quality score.
    """
    semantic_score = score_readme_quality_semantic(repo.get("readme_text", ""))
    structural_score = check_structural_quality(repo)
    combined = (0.7 * semantic_score) + (0.3 * structural_score)
    return int(combined * 100)


def calculate_final_score(skill_match_pct: float, quality_score: int) -> int:
    """
    Merge skill match percentage (from Person 2) with repo quality score.
    Returns a normalized 0–100 final score.
    """
    # Example weighting: 60% skill match, 40% quality
    final = (0.6 * (skill_match_pct / 100)) + (0.4 * (quality_score / 100))
    return int(final * 100)
