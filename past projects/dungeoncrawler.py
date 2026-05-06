"""
APPLICATION DESCRIPTION:
This is a text-based dark fantasy dungeon crawler RPG powered by GPT-4o-mini.
The player names their character and descends into a dangerous dungeon filled with
monsters, traps, and treasure — culminating in a bizarre final boss (a winged giraffe
with a short neck, unicorn horns, and a giant donger). Each turn, the AI Game Master
generates a vivid scene and presents exactly 3 action choices as clickable buttons.
The player's HP, Defense, and Gold stats update based on their decisions, and the game
ends if HP reaches 0.

EXPECTED USER INPUT:
- Character name: A single word or short name (e.g. "LeBron James", "Thorin", "xX_DarkLord_Xx")
- Action selection: The player clicks one of 3 labeled buttons per turn — no typing required
  after the character name is entered.
"""

import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

#This entire portion was from Claude, but I had claude explain the code and how to use it but I suggested the fonts and the colors that are used for the display :)
st.markdown("""
<style>
    /* Title/header with blood-red color and dramatic font size */
    h1 {
        color: #8B0000 !important;
        font-size: 2.8rem !important;
        font-family: 'Georgia', serif !important;
        letter-spacing: 0.1em;
        text-shadow: 2px 2px 8px rgba(139,0,0,0.6);
    }
    h2, h3 {
        color: #C9A84C !important;
        font-family: 'Georgia', serif !important;
    }

    /* Global button styling applied before buttons render */
    .stButton > button {
        background-color: #1a0a00 !important;
        color: #C9A84C !important;
        border: 1px solid #8B0000 !important;
        border-radius: 4px !important;
        font-family: 'Georgia', serif !important;
        font-size: 0.95rem !important;
        padding: 0.5rem 1.2rem !important;
        transition: background-color 0.2s ease, color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #8B0000 !important;
        color: #fff8e7 !important;
        border-color: #C9A84C !important;
    }

    /* Scene container with dark parchment background and gold border */
    .scene-box {
        background-color: #12080a !important;
        border: 2px solid #8B0000 !important;
        border-radius: 6px !important;
        padding: 1.2rem 1.5rem !important;
        color: #e8d5b0 !important;
        font-family: 'Georgia', serif !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
        box-shadow: inset 0 0 20px rgba(139,0,0,0.15);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

#Session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "character_name" not in st.session_state:
    st.session_state.character_name = ""

if "current_scene" not in st.session_state:
    st.session_state.current_scene = ""

if "current_actions" not in st.session_state:
    st.session_state.current_actions = []

if "hp" not in st.session_state:
    st.session_state.hp = 100

if "defense" not in st.session_state:
    st.session_state.defense = 10

if "gold" not in st.session_state:
    st.session_state.gold = 0


#Helpers/prompt asked the AI
def get_system_prompt(character_name):
    return (
        f"You are a Game Master running a dark fantasy dungeon crawler. "
        f"The player's character is named {character_name}. "
        f"The dungeon is grim, dangerous, and full of monsters, traps, and treasure and the final boss is a giraffe with a really short neck and unicorn horns with wings and a giant donger. "
        f"Each turn, describe a scene and give exactly 3 numbered action choices. "
        f"You must respond ONLY in valid JSON with this exact format: "
        f'{{ "scene": "Your scene description here.", "actions": ["Action 1", "Action 2", "Action 3"], '
        f'"hp_change": 0, "defense_change": 0, "gold_change": 0 }} '
        f"hp_change, defense_change, and gold_change should reflect consequences of the previous action (use 0 for the first scene). "
        f"Keep scenes vivid and atmospheric but concise. Never break character."
    )


def generatetopic(character_name, history):
    messages = [{"role": "system", "content": get_system_prompt(character_name)}] + history
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content


def gmresponse1(raw, fallback_actions=None, fallback_hp=0, fallback_defense=0, fallback_gold=0):
    if fallback_actions is None:
        fallback_actions = ["Look around", "Move forward", "Wait and listen"]
    # little bit of AI helped me with the raw = raw.strip section as it helped me get over
    # the hurdle of fallback actions and giving a raw json file.
    try:
        raw = raw.strip().replace("```json", "").replace("```", "")
        return json.loads(raw)
    except:
        return {
            "scene": raw,
            "actions": fallback_actions,
            "hp_change": fallback_hp,
            "defense_change": fallback_defense,
            "gold_change": fallback_gold
        }


#The Title
# AI-assisted styling: used Claude to pick font size and color for the title to feel, it sets the tone more effectively for the player
st.title("ThE DePtHS of tHE aBySs")

#The boot-up screen
if not st.session_state.game_started:
    # Subtitle, its to make it more dramatic and will disappear at the end of the intro screen.
    st.subheader("Fall to either rags or riches, your life depends on your actions.")

    # Text input for character name and used continuously throughout the game
    character_name_input = st.text_input("Enter your character's name:", placeholder="e.g. LeBron James")

    #Button to start the game
    if st.button("Begin?"):
        if character_name_input.strip() == "":
            st.warning("No nameless type shits.")
        else:
            st.session_state.character_name = character_name_input.strip()
            st.session_state.game_started = True
            st.session_state.chat_history = []
            st.session_state.hp = 100
            st.session_state.defense = 10
            st.session_state.gold = 0

            opening_message = {"role": "user", "content": "Begin the dungeon. Describe the entrance and give me my first choices."}
            st.session_state.chat_history.append(opening_message)

            raw = generatetopic(st.session_state.character_name, st.session_state.chat_history)
            data = gmresponse1(raw)

            st.session_state.chat_history.append({"role": "assistant", "content": raw})
            st.session_state.current_scene = data["scene"]
            st.session_state.current_actions = data["actions"]
            st.rerun()

#The Game interface/UI
else:
    character_name = st.session_state.character_name

    # Stats display: HP, Defense, Gold — persists throughout the game
    st.write(f"Victim: {character_name} HP: {st.session_state.hp} DEF: {st.session_state.defense} Gold: {st.session_state.gold}")
    st.markdown("---")

    # AI-assisted styling: used Claude to structure the scene container with a dark background
    # and gold border so the GM narration feels like reading by torchlight.
    # Scene description displayed inside a styled box — visually distinct without a plain label.
    st.markdown(
        f'<div class="scene-box">&nbsp;{st.session_state.current_scene}</div>',
        unsafe_allow_html=True
    )

    st.write("**What do you do?**")

    # Each action displayed as its own button — no text input or number input used.
    # Asked AI help with the suggestions and how to implement and work with the
    # enumerate portion of the code itself and partially of many relevant parts.
    for i, action in enumerate(st.session_state.current_actions):
        if st.button(f"{i+1}. {action}", key=f"action_{i}"):
            player_message = {"role": "user", "content": f"I choose: {action}"}
            st.session_state.chat_history.append(player_message)

            raw = generatetopic(st.session_state.character_name, st.session_state.chat_history)
            data = gmresponse1(raw)

            st.session_state.chat_history.append({"role": "assistant", "content": raw})
            st.session_state.current_scene = data["scene"]
            st.session_state.current_actions = data["actions"]

            st.session_state.hp = max(0, st.session_state.hp + data.get("hp_change", 0))
            st.session_state.defense = max(0, st.session_state.defense + data.get("defense_change", 0))
            st.session_state.gold = max(0, st.session_state.gold + data.get("gold_change", 0))

            if st.session_state.hp <= 0:
                st.session_state.current_scene = "Tough luck kid, you've died. Maybe you'll be luckier as your reincarnation."
                st.session_state.current_actions = []

            st.rerun()

    #Its for a retry button
    if not st.session_state.current_actions and st.session_state.hp > 0:
        st.warning("The dungeon lost its words. Tough-luck bub.")
        if st.button("Stand-up?"):
            raw = generatetopic(st.session_state.character_name, st.session_state.chat_history)
            data = gmresponse1(raw)
            st.session_state.current_scene = data["scene"]
            st.session_state.current_actions = data["actions"]
            st.rerun()

    st.markdown("---")
    if st.button("Scared?"):
        st.session_state.game_started = False
        st.session_state.chat_history = []
        st.session_state.current_scene = ""
        st.session_state.current_actions = []
        st.session_state.hp = 100
        st.session_state.defense = 10
        st.session_state.gold = 0
        st.rerun()