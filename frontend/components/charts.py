import streamlit as st
import pandas as pd

def show_repo_language_chart(repo_data):
    if not repo_data:
        st.warning("No repository data available.")
        return
    
    # Count languages across all repos
    language_counts = {}
    for repo in repo_data:
        tech_stack = repo.get("tech_stack", [])
        for lang in tech_stack:
            language_counts[lang] = language_counts.get(lang, 0) + 1
    
    if language_counts:
        # Convert to DataFrame for chart
        import pandas as pd
        df = pd.DataFrame({
            "Language": list(language_counts.keys()),
            "Count": list(language_counts.values())
        })
        st.bar_chart(df.set_index("Language"))
    else:
        st.info("No language data available.")