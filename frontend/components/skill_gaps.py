import streamlit as st

def show_skill_gaps(skill_gaps):
    st.subheader("Skill Gaps")
    if not skill_gaps:
        st.info("No gaps detected.")
        return
    for skill, importance in skill_gaps.items():
        st.write(f"- **{skill}** (importance: {importance})")
