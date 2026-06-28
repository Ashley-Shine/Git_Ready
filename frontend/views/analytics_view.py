import streamlit as st
from backend.analytics import get_trending_gaps, get_average_score

def show_analytics_view(role: str = None):
    st.title("Analytics Dashboard")

    if not role:
        st.info("Enter a username and role in the sidebar and click Analyze first.")
        return

    st.subheader(f"Trending Skill Gaps — {role}")
    gaps = get_trending_gaps(role)
    if gaps:
        st.bar_chart({skill: i + 1 for i, skill in enumerate(reversed(gaps))})
        st.write("Most commonly missing skills this week:")
        for i, skill in enumerate(gaps, 1):
            st.write(f"{i}. {skill}")
    else:
        st.info("No analytics data yet for this role.")

    st.subheader(f"Average Profile Score — {role}")
    avg = get_average_score(role)
    st.metric(label="Average Score", value=f"{avg}/100")