import streamlit as st

st.title("Simple Streamlit Website")
st.caption("User Input Section")

name = st.text_input("Enter your name")
bio = st.text_area("Describe your project idea")
color = st.selectbox(
    "Choose project type",
    ["Game", "Email Generator", "Translate", "Wiki", "AI Debate"]
)

st.write("Name:", name)
st.write("Category:", bio)
st.write("Idea:", color)

st.caption("Progress")

value = st.slider("Pick a number", 0, 100, key="slider1")
st.progress(value)

if st.button("Click me"):
    st.write("You Clicked me!")