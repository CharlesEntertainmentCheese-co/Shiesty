import os
import streamlit as st
from openai import OpenAI

client = OpenAI(api=st.secrets["OPENAI_API_KEY"])

st.title("Email Generator")
st. header("Your trusty partner to make selfish demands!")

with st.form("creature_form"):
    st.title("Query")
    name = st.text_input("Whats your name?")
    recipient = st.text_input("Whats the recipient name?")
    style = st.text_input("Whats the style you want?")
    topic = st.text_area("Whats the email about?")
    tone = st.multiselect("Pick your tone:", "Angry", "Sad", "Ecstatic")
    length = st.number_input("How many words do you want it to be?", value=0)

    submit = st.form_submit_button("Generate")
