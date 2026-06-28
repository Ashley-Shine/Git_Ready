import streamlit as st

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

    st.subheader(f"Top Required Skills for {role}")
    st.bar_chart(skills)

    st.write("Skills ranked by market demand:")
    for i, (skill, score) in enumerate(
        sorted(skills.items(), key=lambda x: x[1], reverse=True), 1
    ):
        st.progress(score, text=f"{i}. {skill} — {score}")