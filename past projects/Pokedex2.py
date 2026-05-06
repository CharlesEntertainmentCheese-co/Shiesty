import os
import json
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

Saves = "pokedex_entries.json"

# Load saved entries from file if it exists
# AI helped me understand how to use os.path.exists to check before opening
if os.path.exists(Saves):
    with open(Saves, "r") as file:
        pokedex_entries = json.load(file)
else:
    pokedex_entries = {}

st.title("The Pokedex")
st.header("The National Dex!")

with st.form("creature_form"):
    pokemon = st.text_input("Enter the Pokémon's name below")
    submit = st.form_submit_button("Generate")

if submit:
    if pokemon == "":
        st.warning("Please fill in the box first.")
    else:
        # AI helped me structure the messages list format for the OpenAI API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You write short Pokédex entries using the name I provide on the text input."
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
        pokedex_entries[pokemon.title()] = result

        with open(Saves, "w") as file:
            json.dump(pokedex_entries, file, indent=4)

        st.success(f"{pokemon.title()} was added to the Pokédex!")

st.subheader("Saved Pokédex Entries")

if pokedex_entries:
    selected_pokemon = st.radio(
        "Choose a saved Pokémon entry:",
        list(pokedex_entries.keys())
    )

    st.subheader(f"{selected_pokemon}'s Entry")

    # AI helped me understand how to use st.columns to split the display area
    col1, col2 = st.columns(2)

    entry_text = pokedex_entries[selected_pokemon]
    lines = entry_text.strip().split("\n")
    midpoint = len(lines) // 2

    with col1:
        st.write("\n".join(lines[:midpoint]))

    with col2:
        st.write("\n".join(lines[midpoint:]))

else:
    st.write("No Pokédex entries saved yet.")