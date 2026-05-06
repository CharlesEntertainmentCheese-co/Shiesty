import streamlit as st

with st.form("creature_form"):
    col1, col2 = st.columns(2)
    with col1:
        st.title("col1")
    with col2:
        st.title("col2")
submit = st.form_submit_button("Create Creature")
if submit:
    st.write("Hello")