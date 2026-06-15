import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

def test_adzuna(role: str):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": role,
        "results_per_page": 10,
        "content-type": "application/json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Total results: {data.get('count', 0)}")
    print(f"First job title: {data['results'][0]['title']}")
    print(f"Description snippet: {data['results'][0]['description'][:200]}")

test_adzuna("frontend developer")