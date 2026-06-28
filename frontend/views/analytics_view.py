import streamlit as st

def show_analytics_view(result,role):
    st.title("Analytics Results")

    if not result:
        st.info("Enter a username and role in the sidebar and click Analyze first.")
        return

    analytics = result.get("analytics", {})
    trending_gaps = analytics.get("trending_gaps", [])
    average_score = analytics.get("average_score", 0.0)

    st.subheader(f"Trending Skill Gaps — {role}")
    if trending_gaps:
        st.bar_chart({skill: i + 1 for i, skill in enumerate(reversed(trending_gaps))})
        st.write("Most commonly missing skills this week:")
        for i, skill in enumerate(trending_gaps, 1):
            st.write(f"{i}. {skill}")
    else:
        st.info("No analytics data yet for this role.")

    st.subheader(f"Average Profile Score — {role}")
    st.metric(label="Average Score", value=f"{average_score}/100")