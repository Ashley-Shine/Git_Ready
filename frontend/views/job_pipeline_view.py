import streamlit as st

def show_job_pipeline_view(job_data):
    st.title("Job Pipeline")
    if not job_data:
        st.info("No job data available.")
        return
    for posting in job_data:
        st.write(f"- {posting['title']} ({posting['company']})")
