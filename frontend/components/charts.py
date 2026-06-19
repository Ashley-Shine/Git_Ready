import streamlit as st
import pandas as pd

def show_repo_language_chart(repo_data):
    if not repo_data:
        st.warning("No repository data available.")
        return
    df = pd.DataFrame(repo_data)
    if "language" in df.columns:
        st.bar_chart(df["language"].value_counts())
    else:
        st.info("Language data missing.")
