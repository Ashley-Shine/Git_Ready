import streamlit as st

def show_metrics(score, quality_score, skill_match):
    st.metric("Profile Score", f"{score}/100")
    st.metric("Quality Score", f"{quality_score}/100")
    st.metric("Skill Match", f"{skill_match}%")
