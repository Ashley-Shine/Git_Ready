import requests
import streamlit as st

BACKEND_URL = "https://your-backend-url.onrender.com"

def analyze_profile(username: str, role: str):
    try:
        response = requests.get(f"{BACKEND_URL}/analyze", params={"username": username, "role": role})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Backend error: {e}")
        return None
