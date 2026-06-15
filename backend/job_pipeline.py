import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Common tech skills to look for in job descriptions
SKILL_KEYWORDS = [
    "python", "javascript", "typescript", "react", "reactjs", "react.js",
    "node", "nodejs", "node.js", "fastapi", "django", "flask", "express",
    "postgresql", "mysql", "mongodb", "redis", "docker", "kubernetes",
    "aws", "azure", "gcp", "git", "css", "html", "tailwind", "nextjs",
    "next.js", "vue", "angular", "java", "spring", "kotlin", "swift",
    "machine learning", "deep learning", "tensorflow", "pytorch", "sql",
    "rest", "graphql", "linux", "ci/cd", "jenkins", "terraform"
]

def fetch_raw_postings(role: str, pages: int = 5) -> list:
    """
    Fetches raw job postings from Adzuna for a given role.
    pages=5 means 5 x 10 results = 50 job postings
    """
    all_postings = []

    for page in range(1, pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": role,
            "results_per_page": 10,
            "content-type": "application/json"
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error on page {page}: {response.status_code}")
            continue

        data = response.json()
        results = data.get("results", [])

        if not results:
            print(f"No results on page {page}, stopping.")
            break

        all_postings.extend(results)
        print(f"Fetched page {page} — total postings so far: {len(all_postings)}")

    return all_postings


def extract_skills_from_text(text: str) -> list:
    """
    Looks for known skill keywords inside a job description text.
    Returns a list of skill mentions found.
    """
    text_lower = text.lower()
    found_skills = []

    for skill in SKILL_KEYWORDS:
        # Check if skill word appears in the text
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.append(skill)

    return found_skills


def fetch_job_postings(role: str) -> list:
    """
    Main function — fetches postings and extracts all skill mentions.
    Returns one flat list of all skill strings found across all postings.
    """
    print(f"\nFetching job postings for: {role}")
    postings = fetch_raw_postings(role)

    if not postings:
        print("No postings found.")
        return []

    all_skills = []

    for posting in postings:
        description = posting.get("description", "")
        title = posting.get("title", "")

        # Combine title + description for better skill extraction
        full_text = title + " " + description
        skills = extract_skills_from_text(full_text)
        all_skills.extend(skills)

    print(f"\nTotal skill mentions extracted: {len(all_skills)}")
    print(f"Unique skills found: {list(set(all_skills))}")

    return all_skills