import streamlit as st

def show_sidebar():
    st.sidebar.title("GitReady")
    st.sidebar.markdown("Analyze your GitHub profile against job market trends.")
    username = st.sidebar.text_input("GitHub Username")
    role = st.sidebar.text_input("Target Role (e.g., Backend Developer)")
    analyze = st.sidebar.button("Analyze Profile")
    return username, role, analyze
