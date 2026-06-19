import streamlit as st
from components.sidebar import show_sidebar
from utils.api_client import analyze_profile
from pages.dashboard import show_dashboard
from pages.analytics_view import show_analytics_view
from pages.job_pipeline_view import show_job_pipeline_view
from pages.skills_taxonomy_view import show_skills_taxonomy_view

def main():
    username, role, analyze = show_sidebar()
    st.sidebar.markdown("---")
    st.sidebar.markdown("Navigate:")
    page = st.sidebar.radio("Select View", ["Dashboard", "Analytics", "Job Pipeline", "Skills Taxonomy"])

    result = None
    if analyze and username and role:
        result = analyze_profile(username, role)

    if page == "Dashboard":
        show_dashboard(result)
    elif page == "Analytics":
        show_analytics_view(result.get("analytics") if result else None)
    elif page == "Job Pipeline":
        show_job_pipeline_view(result.get("job_data") if result else None)
    elif page == "Skills Taxonomy":
        show_skills_taxonomy_view(result.get("taxonomy") if result else None)

if __name__ == "__main__":
    main()
