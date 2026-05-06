import streamlit as st

st.title("Mood Movie Picker")
st.radio("How are you feeling?", "Happy", "Sad", "Excited", "Bored", "Scared")

col1, col2 = st.columns(2)
with col1:
    Happy = "Happy"
    Excited = "Excited"
    Sad = "Sad"
    Bored = "Bored"
    Scared = "Scared"
    st.radio("How are you feeling?", Happy, Sad, Excited, Bored, Scared)
with col2:
    if Happy == True:
        st.title("The Secret Life of Pets")
        st.print("A fun lighthearted animated comedy.")