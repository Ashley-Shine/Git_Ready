import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from collections import Counter
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load the embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def embed_skills(skills: list) -> np.ndarray:
    """
    Converts a list of skill strings into vectors using sentence-transformers.
    Example: ["react", "reactjs"] → [[0.23, 0.87, ...], [0.24, 0.86, ...]]
    """
    print("Embedding skills...")
    embeddings = model.encode(skills, show_progress_bar=True)
    return embeddings


def cluster_skills(skills: list, embeddings: np.ndarray, n_clusters: int = 15) -> dict:
    """
    Groups similar skill embeddings into clusters using KMeans.
    Returns a dict mapping cluster_id → list of skills in that cluster.
    """
    print(f"Clustering into {n_clusters} clusters...")

    # KMeans groups similar vectors together
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    # Group skills by their cluster label
    clusters = {}
    for skill, label in zip(skills, labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(skill)

    return clusters


def build_taxonomy_with_embeddings(role: str, raw_skills: list) -> dict:
    
    role = role.lower()  # add this as first line
    # rest of the function stays the same
    """
    Main function — takes raw skill mentions and builds a clean taxonomy.
    Saves result to Supabase and returns the taxonomy dict.
    """
    if not raw_skills:
        print("No skills provided.")
        return {}

    # Step 1 — Count raw frequency of each skill mention
    skill_counts = Counter(raw_skills)
    unique_skills = list(skill_counts.keys())

    print(f"\nUnique skills before clustering: {len(unique_skills)}")

    # Step 2 — Embed all unique skills
    embeddings = embed_skills(unique_skills)

    # Step 3 — Cluster similar skills together
    # Use fewer clusters if we have fewer unique skills
    n_clusters = min(15, len(unique_skills) // 2)
    clusters = cluster_skills(unique_skills, embeddings, n_clusters)

    # Step 4 — For each cluster, pick the most frequent skill as the name
    # and sum up the total frequency count
    taxonomy_raw = {}
    for cluster_id, cluster_skills_list in clusters.items():
        # Pick the skill that appeared most as the cluster name
        representative = max(cluster_skills_list, key=lambda s: skill_counts[s])
        total_count = sum(skill_counts[s] for s in cluster_skills_list)
        taxonomy_raw[representative] = total_count

    # Step 5 — Normalize counts to 0-1 range
    max_count = max(taxonomy_raw.values())
    taxonomy_normalized = {
        skill: round(count / max_count, 2)
        for skill, count in taxonomy_raw.items()
    }

    # Sort by score descending
    taxonomy_sorted = dict(
        sorted(taxonomy_normalized.items(), key=lambda x: x[1], reverse=True)
    )

    # Step 6 — Build final taxonomy object
    taxonomy = {
        "role": role,
        "skills": taxonomy_sorted
    }

    print(f"\nFinal taxonomy for '{role}':")
    for skill, score in taxonomy_sorted.items():
        print(f"  {skill}: {score}")

    # Step 7 — Save to Supabase
    save_taxonomy_to_supabase(taxonomy)

    return taxonomy


def save_taxonomy_to_supabase(taxonomy: dict):
    """
    Saves the taxonomy to Supabase taxonomy table.
    If role already exists, updates it.
    """
    try:
        # Check if role already exists
        existing = supabase.table("taxonomy").select("*").eq("role", taxonomy["role"]).execute()

        if existing.data:
            # Update existing record
            supabase.table("taxonomy").update({
                "skills": taxonomy["skills"],
                "updated_at": "now()"
            }).eq("role", taxonomy["role"]).execute()
            print(f"Updated taxonomy for '{taxonomy['role']}' in Supabase")
        else:
            # Insert new record
            supabase.table("taxonomy").insert({
                "role": taxonomy["role"],
                "skills": taxonomy["skills"]
            }).execute()
            print(f"Saved taxonomy for '{taxonomy['role']}' to Supabase")

    except Exception as e:
        print(f"Supabase error: {e}")


def get_taxonomy_from_supabase(role: str) -> dict:
    try:
        role_lower = role.lower().strip()  # always lowercase
        result = supabase.table("taxonomy").select("*").eq("role", role_lower).execute()
        if result.data:
            return result.data[0]
        else:
            print(f"No taxonomy found for role: {role}")
            return {}
    except Exception as e:
        print(f"Supabase error: {e}")
        return {}
def refresh_taxonomy(role: str) -> dict:
    """
    Forces a fresh fetch from Adzuna and rebuilds the taxonomy.
    """
    from backend.job_pipeline import fetch_job_postings
    
    role = role.lower().strip()
    print(f"Refreshing taxonomy for '{role}' from live Adzuna data...")
    
    raw_skills = fetch_job_postings(role)
    
    if not raw_skills:
        print(f"No skills found for role: {role}")
        return {}
    
    return build_taxonomy_with_embeddings(role, raw_skills)