import streamlit as st
from groq import Groq


# Get API key from Streamlit Cloud Secrets
api_key = st.secrets["GROQ_API_KEY"]


client = Groq(
    api_key=api_key
)
