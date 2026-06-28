import requests
import os
import base64
from groq import Groq
import json
from dotenv import load_dotenv

# Added error handling for GitHub API responses
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

HEADERS = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}

def get_user_repos(username: str):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers=HEADERS, params={"per_page": 100})
    #BELOW WAS NOT THERE
    if response.status_code != 200:
        return []
    payload = response.json()
    if isinstance(payload, list):
        return payload
    return []
#TILL HERE
def get_readme(username:str, repo_name: str):
    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        import base64
        content = response.json()["content"]
        return base64.b64decode(content).decode("utf-8", errors="ignore")
    return ""    
def get_languages(username: str, repo_name: str):
    url = f"https://api.github.com/repos/{username}/{repo_name}/languages"
    response = requests.get(url, headers=HEADERS)
    return response.json()
def fetch_github_profile(username: str):
    repos = get_user_repos(username)
    profile_data = []
    
    for repo in repos:
       #BELOW WAS NOT THERE
        if not isinstance(repo, dict):
            continue
        repo_name = repo.get("name")
        if not repo_name:
            continue
       #TILL HERE
        profile_data.append({
            "name": repo_name,
            "readme_text": get_readme(username, repo_name),
            "languages": get_languages(username, repo_name),
            "stars": repo.get("stargazers_count", 0),
            "has_tests": False,
            "has_ci": False,
            "license": repo.get("license", {}).get("name") if repo.get("license") else None,
        })
    
    return profile_data

def clean_repo_with_llm(repo_data: dict) -> dict:
    prompt = f"""
You are analyzing a GitHub repository.

Repo name: {repo_data.get('name', 'unknown')}
Languages: {repo_data.get('languages', {})}
README preview: {repo_data.get('readme_text', '')[:1000]}

Extract:
1. tech_stack: list of programming languages, frameworks, and technologies used
2. purpose: one sentence describing what this project does

Return ONLY valid JSON in this exact format:
{{"tech_stack": ["Python", "FastAPI"], "purpose": "A web app for tracking habits"}}
"""
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    
    try:
        content = response.choices[0].message.content.strip()
        
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        content = content.strip()
        result = json.loads(content)
        
        return {
            "tech_stack": result.get("tech_stack", []),
            "purpose": result.get("purpose", "")
        }
    except:
        return {"tech_stack": [], "purpose": ""}

def get_cleaned_profile(username: str) -> list:
    raw_data = fetch_github_profile(username)
    cleaned_profiles = []
    
    for repo in raw_data:
        llm_result = clean_repo_with_llm(repo)
        repo_name = repo["name"]
        cleaned_repo = {
            "name": repo["name"],
            "tech_stack": llm_result["tech_stack"],
            "purpose": llm_result["purpose"],
            "readme_text": repo["readme_text"],
            "has_tests": check_has_tests(username,repo_name),
            "has_ci": check_has_ci(username, repo_name),
            "license": repo["license"],
            "commit_dates": get_commit_dates(username,repo_name),
            "contributors": get_contributor_count(username,repo_name)
        }
        cleaned_profiles.append(cleaned_repo)
    
    return cleaned_profiles
def check_has_tests(username: str, repo_name: str) -> bool:
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return False
    
    items = response.json()
    if not isinstance(items, list):
        return False
    
    for item in items:
        name = item.get("name", "").lower()
        if name == "tests" or name == "test" or name.startswith("test_") or name.endswith("_test"):
            return True
    return False
def check_has_ci(username: str, repo_name: str) -> bool:
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents/.github/workflows"
    response = requests.get(url, headers=HEADERS)
    return response.status_code == 200
def get_commit_dates(username: str, repo_name: str, limit: int = 10) -> list:
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    response = requests.get(url, headers=HEADERS, params={"per_page": limit})
    if response.status_code != 200:
        return []
    
    commits = response.json()
    if not isinstance(commits, list):
        return []
    
    dates = []
    for commit in commits:
        date = commit.get("commit", {}).get("author", {}).get("date")
        if date:
            dates.append(date.split("T")[0])
    return dates
def get_contributor_count(username: str, repo_name: str) -> int:
    url = f"https://api.github.com/repos/{username}/{repo_name}/contributors"
    response = requests.get(url, headers=HEADERS, params={"per_page": 1})
    if response.status_code != 200:
        return 0
    
    contributors = response.json()
    if isinstance(contributors, list):
        return len(contributors)
    return 0

def get_last_push_date(username: str) -> str:
    try:
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url, headers=HEADERS, params={"per_page": 100, "sort": "pushed"})
        if response.status_code != 200:
            return None
        repos = response.json()
        if not repos or not isinstance(repos, list) or len(repos) == 0:
            return None
        for repo in repos:
            pushed_at = repo.get("pushed_at")
            if pushed_at:
                return pushed_at
        return None
    except Exception as e:
        print(f"Error getting last push: {e}")
        return None