import streamlit as st
from backend.skills_taxonomy import get_taxonomy_from_supabase

def show_skills_taxonomy_view(role: str = None):
    st.title("Skills Taxonomy")

    if not role:
        st.info("Enter a role in the sidebar to see its taxonomy.")
        return

    taxonomy = get_taxonomy_from_supabase(role.lower().strip())

    if not taxonomy or "skills" not in taxonomy:
        st.warning(f"No taxonomy found for '{role}'. Try refreshing.")
        return

    st.subheader(f"Required Skills for {role}")
    skills = taxonomy["skills"]

    # Bar chart
    st.bar_chart(skills)

    # Table
    st.write("Skills ranked by market demand:")
    for skill, score in sorted(skills.items(), key=lambda x: x[1], reverse=True):
        st.progress(score, text=f"{skill}: {score}")