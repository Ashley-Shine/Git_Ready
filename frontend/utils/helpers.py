import streamlit as st

def show_section_header(title: str):
    st.markdown(f"### {title}")

def show_divider():
    st.markdown("---")
