from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_skills(cleaned_repos: list, taxonomy: dict) -> dict: 
    """
    Compare user's repo tech stack against role taxonomy.
    Returns matched skills and missing skills with scores.
    """
    role_skills = list(taxonomy["skills"].keys())
    role_weights = list(taxonomy["skills"].values())

    # embed taxonomy skills
    taxonomy_embeddings = model.encode(role_skills)

    # build FAISS index from taxonomy
    index = faiss.IndexFlatL2(taxonomy_embeddings.shape[1])
    index.add(taxonomy_embeddings)

    # collect all skills from user's repos
    user_skills = []
    for repo in cleaned_repos:
        user_skills.extend(repo.get("tech_stack", []))
    user_skills = list(set(user_skills))  # deduplicate

    if not user_skills:
        return {"matched": [], "missing": role_skills}

    # embed user skills and search
    user_embeddings = model.encode(user_skills)
    distances, indices = index.search(user_embeddings, 1)

    matched = []
    matched_indices = set()

    for i, (dist, idx) in enumerate(zip(distances, indices)):
        if dist[0] < 1.0:  # similarity threshold
            matched.append({
                "skill": role_skills[idx[0]],
                "matched_by": user_skills[i],
                "importance": role_weights[idx[0]]
            })
            matched_indices.add(idx[0])

    missing = [
        {"skill": role_skills[i], "importance": role_weights[i]}
        for i in range(len(role_skills))
        if i not in matched_indices
    ]

    # sort both by importance
    matched.sort(key=lambda x: x["importance"], reverse=True)
    missing.sort(key=lambda x: x["importance"], reverse=True)

    return {"matched": matched, "missing": missing}


if __name__ == "__main__":
    from sys import path
    path.append(".")
    from shared.schemas import SAMPLE_CLEANED_REPO, SAMPLE_TAXONOMY

    result = extract_skills([SAMPLE_CLEANED_REPO], SAMPLE_TAXONOMY)

    print("Matched skills:")
    for s in result["matched"]:
        print(f"  {s['skill']} (via {s['matched_by']}, importance: {s['importance']})")

    print("\nMissing skills:")
    for s in result["missing"]:
        print(f"  {s['skill']} (importance: {s['importance']})")