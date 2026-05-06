import os
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
with st.form("creature_form"):
    #Title
    st.title("The Pokedex")
    #Header/Subtitle
    st.header("the National Dex!")
    #Text Input
    pokemon = st.text_input("Enter the Pokémon's name below")
    submit = st.form_submit_button("Generate")

if submit:
    if pokemon == "":
        st.warning("Please fill in all the boxes first.")
    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You write short Pokédex entries using the name I provide on the text_input."
                },
                {
                    "role": "user",
                    "content": f"""
    Write a short pokedex entry about {pokemon}.

    Include:
    Dex number (make it random and not overlapping with existing dex numbers)
    Stats
    Details
    Type
    Weakness
    Evolutions (make it a 3 stage evolution)

    Keep it short and clear.
    """
                }
            ]
        )
    result = response.choices[0].message.content
    st.subheader("Generated Email")
    st.write(result)