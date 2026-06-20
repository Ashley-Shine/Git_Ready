import streamlit as st
def show_skill_gaps(skill_gaps):
    if not skill_gaps:
        st.info("No gaps detected.")
        return

    for gap in skill_gaps:
        if isinstance(gap, dict):
            st.write(f"- **{gap['skill']}** (importance: {gap['importance']})")
        else:
            # Fallback for older string-based data
            st.write(f"- {gap}")
