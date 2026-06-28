import streamlit as st

def show_analytics_view(analytics_data):
    st.title("Analytics Overview")
    if not analytics_data:
        st.info("No analytics data available.")
        return
    for role, gap in analytics_data.items():
        st.write(f"**{role}** → Most common missing skill: {gap}")
