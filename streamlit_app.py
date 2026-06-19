import streamlit as st
from frontend.utils.api_client import analyze_profile
import pandas as pd
import altair as alt

st.set_page_config(page_title="SmartGitProfile Analyzer", layout="wide")
st.title("SmartGitProfile Analyzer")

# Input fields
username = st.text_input("Enter GitHub username:")
role = st.selectbox("Select role:", ["Frontend Developer", "Backend Developer", "Data Scientist"])

# Call backend
if st.button("Analyze"):
    result = analyze_profile(username, role)

    if "error" in result:
        st.error(f"Backend error: {result['error']}")
    else:
        # Show summary metrics
        st.subheader("Profile Summary")
        cols = st.columns(3)
        cols[0].metric("Username", result.get("username", "-"))
        cols[1].metric("Role", result.get("role", "-"))
        cols[2].metric("Total Repos", result.get("total_repos", "-"))

        # Show repositories table
        repos = result.get("repos", [])
        if repos:
            df = pd.DataFrame(repos)
            st.subheader("Repositories Overview")
            st.dataframe(df)

            # Chart: Languages used
            if "language" in df.columns:
                lang_chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X("language:N", title="Language"),
                    y=alt.Y("count():Q", title="Number of Repositories"),
                    color="language:N"
                ).properties(title="Languages Used Across Repositories")
                st.altair_chart(lang_chart, use_container_width=True)

            # Chart: Stars per repo
            if "stars" in df.columns:
                stars_chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X("name:N", title="Repository"),
                    y=alt.Y("stars:Q", title="Stars"),
                    color="name:N"
                ).properties(title="Stars per Repository")
                st.altair_chart(stars_chart, use_container_width=True)

        # Show skill gaps
        st.subheader("Skill Gaps")
        skill_gaps = result.get("skill_gaps", [])
        if not skill_gaps:
            st.write("No skill gaps detected.")
        else:
            for gap in skill_gaps:
                st.write(f"- {gap}")
