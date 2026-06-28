import streamlit as st

def show_skills_taxonomy_view(taxonomy):
    st.title("Skills Taxonomy")
    if not taxonomy:
        st.info("No taxonomy data available.")
        return
    for skill, weight in taxonomy.items():
        st.write(f"{skill}: {weight}")
