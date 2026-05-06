import streamlit as st

st.title("Mythical Creature Profile Builder")
st.header("Design your own legendary being")

with st.form("creature_form"):
    col1, col2 = st.columns(2)
    with col1:
        st.title("Creature Name")
        name = st.text_input("Creature Name")
        origin = st.text_input("World of Origin")
    with col2:
        st.title("Creature Type")
        type = st.selectbox(
            "Creature Type",
            ["Dragon","Spirit","Alien","Robot","Unknown"],
            )
        personality = st.radio("Pick:", options=["Aggressive", "Calm", "Mysterious", "Chaotic"])
        Age = st.number_input(
            "Enter your age",
            value=500
        )
    Choices = st.multiselect(
        "Select Special Abilities:",
        ["Flight", "Fire Breath", "Invisibility", "Telekinesis", "Pyrokinesis", "Shape-shifting"]
    )
    io = st.text_area("Write a short backstory")
    
    agree = st.checkbox("Include a weakness")
    if agree:
        weaknessPolicy = st.text_area("What is the creature weak to?")

    submit = st.form_submit_button("Create Creature")
    if submit: 
        if not name or not origin or not Age or not type or not Choices or not io or not agree:
            st.error("Please fill in all fields.")
        else:
            st.success("Creature Profile Generated!")
            st.write("Name: ", name)
            st.write("Origin: ", origin)
            st.write("Type: ", type)
            st.write("Personality: ", personality)
            st.write("Age: ", Age)
            st.write("Abilities: ", Choices)
            st.warning("Backstory: ", weaknessPolicy)
            
            
