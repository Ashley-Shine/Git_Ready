import streamlit as st
from components.sidebar import show_sidebar
from utils.api_client import analyze_profile
from views.dashboard import show_dashboard
from views.analytics_view import show_analytics_view
from views.job_pipeline_view import show_job_pipeline_view
from views.skills_taxonomy_view import show_skills_taxonomy_view

def main():
    # ✅ Initialize session state for persistent result
    if "result" not in st.session_state:
        st.session_state.result = None

    username, role, analyze = show_sidebar()
    st.sidebar.markdown("---")
    st.sidebar.markdown("Navigate:")
    page = st.sidebar.radio("Select View", ["Dashboard", "Analytics", "Job Pipeline", "Skills Taxonomy"])

    # ✅ Store analysis result in session state to persist across tabs
    if analyze and username and role:
        st.session_state.result = analyze_profile(username, role)

    result = st.session_state.result

    # ✅ Render views using persisted result
    if page == "Dashboard":
        show_dashboard(result)
    elif page == "Analytics":
        show_analytics_view(result=result, role=role)
    elif page == "Job Pipeline":
        show_job_pipeline_view(result=result, role=role)
    elif page == "Skills Taxonomy":
        show_skills_taxonomy_view(result=result, role=role)

if __name__ == "__main__":
    main()
