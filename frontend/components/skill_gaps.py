import streamlit as st

def show_skill_gaps(skill_gaps):
    st.subheader("Skill Gaps")
    if not skill_gaps:
        st.info("No gaps detected.")
        return
    for gap in skill_gaps:
        st.write(f"- **{gap['skill']}** (importance: {gap['importance']})")