import streamlit as st
import pandas as pd

def show_repo_language_chart(repo_data):
    if not repo_data:
        st.warning("No repository data available.")
        return

    # Count how many repos use each language
    language_counts = {}
    for repo in repo_data:
        # Prefer GitHub API 'languages' dict if available
        langs = repo.get("languages", {})
        if isinstance(langs, dict) and langs:
            for lang in langs.keys():
                # Count this repo once for the language
                language_counts[lang] = language_counts.get(lang, 0) + 1
        else:
            # Fallback to tech_stack list if languages dict is missing
            tech_stack = repo.get("tech_stack", [])
            for lang in set(tech_stack):  # use set to avoid double-counting same lang in one repo
                language_counts[lang] = language_counts.get(lang, 0) + 1

    if language_counts:
        df = pd.DataFrame({
            "Language": list(language_counts.keys()),
            "Repo Count": list(language_counts.values())
        })
        st.bar_chart(df.set_index("Language"))
    else:
        st.info("No language data available.")
