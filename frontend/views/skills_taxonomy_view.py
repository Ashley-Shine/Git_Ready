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

    # Show as progress bars with percentage
    st.write("Skills ranked by market demand:")
    for skill, score in sorted(skills.items(), key=lambda x: x[1], reverse=True):
        st.progress(score, text=f"{skill.capitalize()}: {round(score * 100)}% market demand")

    st.divider()

    # Show raw importance scores as table
    st.subheader("Importance Scores")
    import pandas as pd
    df = pd.DataFrame({
        "Skill": [s.capitalize() for s in skills.keys()],
        "Importance Score": list(skills.values())
    }).sort_values("Importance Score", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)