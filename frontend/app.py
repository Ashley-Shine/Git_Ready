import streamlit as st
from components.sidebar import show_sidebar
from utils.api_client import analyze_profile
from views.dashboard import show_dashboard
from views.analytics_view import show_analytics_view
from views.job_pipeline_view import show_job_pipeline_view
from views.skills_taxonomy_view import show_skills_taxonomy_view

def main():
    # Initialize session state for result
    if "result" not in st.session_state:
        st.session_state.result = None

    username, role, analyze = show_sidebar()
    st.sidebar.markdown("---")
    st.sidebar.markdown("Navigate:")
    page = st.sidebar.radio("Select View", ["Dashboard", "Analytics", "Job Pipeline", "Skills Taxonomy"])

    # Run analysis only when requested
    if analyze and username and role:
        st.session_state.result = analyze_profile(username, role)

    # Use persisted result
    result = st.session_state.result

    if page == "Dashboard":
        show_dashboard(result)
    elif page == "Analytics":
        show_analytics_view(result,role)
    elif page == "Job Pipeline":
        show_job_pipeline_view(result.get("job_data") if result else None)
    elif page == "Skills Taxonomy":
        show_skills_taxonomy_view(result.get("taxonomy") if result else None)

if __name__ == "__main__":
    main()
