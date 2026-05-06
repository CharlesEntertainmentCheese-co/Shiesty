import streamlit as st
from openai import OpenAI
# pip install openai

client = OpenAI(api=st.secrets["OPENAI_API_KEY"])