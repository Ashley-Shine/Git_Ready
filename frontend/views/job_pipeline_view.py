import streamlit as st
import pandas as pd

def show_job_pipeline_view(result: dict = None, role: str = None):
    st.title("Job Market Pipeline")

    if not result:
        st.info("Enter a username and role in the sidebar and click Analyze first.")
        return

    taxonomy = result.get("taxonomy", {})
    skills = taxonomy.get("skills", {})

    if not skills:
        st.warning("No job market data available for this role.")
        return

    st.subheader(f"Live Job Market Demand — {role}")
    st.write("Skills ranked by how frequently they appear in real job postings:")

    # Bar chart
    st.bar_chart(skills)

    st.divider()

    # Ranked list with demand level labels
    st.subheader("Skill Demand Breakdown")
    for skill, score in sorted(skills.items(), key=lambda x: x[1], reverse=True):
        if score >= 0.7:
            demand = "🔴 High Demand"
        elif score >= 0.4:
            demand = "🟡 Medium Demand"
        else:
            demand = "🟢 Low Demand"
        st.write(f"**{skill.capitalize()}** — {demand} ({round(score * 100)}%)")