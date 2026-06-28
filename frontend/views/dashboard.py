import streamlit as st
from components.charts import show_repo_language_chart
from components.metrics import show_metrics
from components.skill_gaps import show_skill_gaps
import altair as alt
import pandas as pd

def show_dashboard(result):
    st.title("GitReady Analysis Report")

    # Handle empty result
    if not result:
        st.info("Run an analysis to view results.")
        return

    # 🔹 Display main metrics
    st.subheader("Profile Summary")
    cols = st.columns(3)

    # Skill Match %
    skill_score = result.get("skill_score", result.get("skill_match_pct", "-"))
    if isinstance(skill_score, (int, float)):
        skill_score = round(skill_score, 2)
    cols[0].metric("Skill Match %", skill_score)

    # Quality Score (rounded to 2 decimals)
    quality_score = result.get("quality_score", "-")
    if isinstance(quality_score, (int, float)):
        quality_score = round(quality_score, 2)
    cols[1].metric("Quality Score", quality_score)

    # Final Score (rounded to 2 decimals)
    final_score = result.get("final_score", result.get("score", "-"))
    if isinstance(final_score, (int, float)):
        final_score = round(final_score, 2)
    cols[2].metric("Final Score", final_score)

    # 🔹 Comparison chart
    st.subheader("Skill Match vs. Quality Score")
    chart_data = pd.DataFrame({
        "Metric": ["Skill Match", "Quality Score", "Final Score"],
        "Score": [
            result.get("skill_score", result.get("skill_match_pct", 0)),
            round(result.get("quality_score", 0), 2),
            round(result.get("final_score", result.get("score", 0)), 2)
        ]
    })
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X("Metric:N", title="Metric"),
        y=alt.Y("Score:Q", title="Score"),
        color="Metric:N"
    ).properties(height=300)
    st.altair_chart(chart, use_container_width=True)

    # 🔹 Repository insights
    st.subheader("Repository Insights")
    show_repo_language_chart(result.get("repos"))

    # 🔹 Skill gaps
    st.subheader("Skill Gaps")
    show_skill_gaps(result.get("skill_gaps"))

    # 🔹 Best Repositories
    st.subheader("Best Repositories")
    repos = result.get("repos", [])
    if repos:
        # Sort by quality_score (highest first)
        sorted_repos = sorted(repos, key=lambda x: x.get("quality_score", 0), reverse=True)
        for repo in sorted_repos[:5]:
            st.write(f"**{repo['name']}** — Quality: {repo.get('quality_score', 0)}/100")
            if repo.get("tech_stack"):
                st.write(f"Tech: {', '.join(repo['tech_stack'])}")
            st.write("---")
    else:
        st.info("No repository data available.")
