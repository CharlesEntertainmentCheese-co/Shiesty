import streamlit as st

st.title("Identification")
st.caption("mini profile information")

name = st.text_input("Enter your name")
bio = st.text_area("Summary")
color = st.selectbox("Favorite color", ["red", "blue", "green"])

st.write("Name:", name)
st.write("Bio:", bio)
st.write("Color:", color)

st.image("Lebron.jpg")

