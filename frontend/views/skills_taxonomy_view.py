import streamlit as st

def show_skills_taxonomy_view(result: dict = None, role: str = None):
    st.title("Skills Taxonomy")

    if not result:
        st.info("Enter a username and role in the sidebar and click Analyze first.")
        return

    taxonomy = result.get("taxonomy", {})

    if not taxonomy or "skills" not in taxonomy:
        st.warning(f"No taxonomy found for '{role}'.")
        return

    st.subheader(f"Required Skills for {role}")
    skills = taxonomy["skills"]

    st.bar_chart(skills)

    st.write("Skills ranked by market demand:")
    for skill, score in sorted(skills.items(), key=lambda x: x[1], reverse=True):
        st.progress(score, text=f"{skill}: {score}")