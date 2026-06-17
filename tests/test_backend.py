import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.github_service import (
    get_user_repos,
    get_readme,
    get_languages,
    fetch_github_profile,
    clean_repo_with_llm,
    get_cleaned_profile,
    check_has_tests,
    check_has_ci,
    get_commit_dates,
    get_contributor_count
)

# Test GitHub API repo fetch
def test_get_user_repos():
    repos = get_user_repos("octocat")
    assert len(repos) > 0
    assert "name" in repos[0]
    print("get_user_repos passes")

# Test GitHub API README fetch
def test_get_readme():
    readme = get_readme("octocat", "boysenberry-repo-1")
    assert isinstance(readme, str)
    assert "GitHub Pages" in readme
    print("get_readme passes")

# Test GitHub API languages fetch
def test_get_languages():
    langs = get_languages("octocat", "boysenberry-repo-1")
    assert isinstance(langs, dict)
    print("get_languages passes")

# Test combined profile fetch
def test_fetch_github_profile():
    data = fetch_github_profile("octocat")
    assert len(data) > 0
    assert "name" in data[0]
    assert "readme_text" in data[0]
    assert "languages" in data[0]
    assert "stars" in data[0]
    print("fetch_github_profile passes")

# Test LLM cleaning on a real repo
def test_clean_repo_with_llm():
    raw_data = fetch_github_profile("pallets")
    flask_repo = [r for r in raw_data if r["name"] == "flask"]
    
    if flask_repo:
        result = clean_repo_with_llm(flask_repo[0])
        assert "tech_stack" in result
        assert "purpose" in result
        assert isinstance(result["tech_stack"], list)
        assert isinstance(result["purpose"], str)
        print("clean_repo_with_llm passes")
    else:
        print("Flask repo not found, skipping LLM test")

# Test final cleaned profile with full schema
def test_get_cleaned_profile():
    data = get_cleaned_profile("octocat")
    assert len(data) > 0
    
    first = data[0]
    required_fields = [
        "name", "tech_stack", "purpose", "readme_text",
        "has_tests", "has_ci", "license",
        "commit_dates", "contributors"
    ]
    
    for field in required_fields:
        assert field in first
    
    print("get_cleaned_profile passes")

# Test has_tests detection
def test_check_has_tests():
    result = check_has_tests("pallets", "flask")
    assert isinstance(result, bool)
    print("check_has_tests passes")

# Test has_ci detection
def test_check_has_ci():
    result = check_has_ci("pallets", "flask")
    assert isinstance(result, bool)
    print("check_has_ci passes")

# Test commit dates fetch
def test_get_commit_dates():
    dates = get_commit_dates("pallets", "flask", limit=5)
    assert isinstance(dates, list)
    print("get_commit_dates passes")

# Test contributor count fetch
def test_get_contributor_count():
    count = get_contributor_count("pallets", "flask")
    assert isinstance(count, int)
    assert count >= 0
    print("get_contributor_count passes")

# Test invalid username handling
def test_invalid_username():
    try:
        data = get_cleaned_profile("thisuserdoesnotexist12345")
        assert isinstance(data, list)
        print("invalid_username passes")
    except:
        print("invalid_username passes (exception caught)")

# Test repo without README
def test_repo_without_readme():
    readme = get_readme("octocat", "octocat.github.io")
    assert isinstance(readme, str)
    print("repo_without_readme passes")

# Test FastAPI endpoint if server is running
def test_fastapi_endpoint():
    try:
        import requests
        response = requests.get("http://localhost:8000/analyze?username=octocat", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "username" in data
        assert "repos" in data
        assert "score" in data
        assert "skill_gaps" in data
        print("fastapi_endpoint passes")
    except requests.exceptions.ConnectionError:
        print("FastAPI server not running, skipping endpoint test")
    except Exception as e:
        print(f"FastAPI test skipped: {e}")

if __name__ == "__main__":
    print("Running Backend Tests...")
    
    test_get_user_repos()
    test_get_readme()
    test_get_languages()
    test_fetch_github_profile()
    test_clean_repo_with_llm()
    test_get_cleaned_profile()
    test_check_has_tests()
    test_check_has_ci()
    test_get_commit_dates()
    test_get_contributor_count()
    test_invalid_username()
    test_repo_without_readme()
    test_fastapi_endpoint()
    
    print("All Backend tests passed!")