import streamlit as st
from components.charts import show_repo_language_chart
from components.metrics import show_metrics
from components.skill_gaps import show_skill_gaps

def show_dashboard(result):
    st.title("GitReady Dashboard")
    if not result:
        st.info("Run an analysis to view results.")
        return
    show_metrics(result["score"], result["quality_score"], result["skill_match_pct"])
    show_repo_language_chart(result.get("top_repos"))
    show_skill_gaps(result.get("skill_gaps"))
