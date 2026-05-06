import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Had Claude help me out with the size and parameters of the button with the st_yled.set portions.
# (removed st_yled.set calls - no longer using st_yled)

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
    messages = [{"role": "system", "content": get_system_prompt(character_name)}] + history  # fixed: was calling itself
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

def gmresponse1(raw, fallback_actions=None, fallback_hp=0, fallback_defense=0, fallback_gold=0):
    if fallback_actions is None:
        fallback_actions = ["Look around", "Move forward", "Wait and listen"]
    # little bit of AI helped me with the raw = raw.strip section as it help me get over the hurdle of fallback actions and giving a raw json file.
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

# AI-assisted styling: used Claude to pick font size and color for the title to feel dramatic and set the dungeon tone immediately, along with some tips on displays within the 
# actual code's final results itself like the "placeholder"
st.title("ThE DePtHS of tHE aBySs")

if not st.session_state.game_started:
    st.subheader("Fall to either rags or riches, your life depends on your actions.")

    character_name_input = st.text_input("Enter your character's name:", placeholder="e.g. LeBron James")

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

else:
    character_name = st.session_state.character_name

    st.write(f"Hero: {character_name} | HP: {st.session_state.hp} | DEF: {st.session_state.defense} | Gold: {st.session_state.gold}")
    st.markdown("---")

    # AI-assisted styling: used Claude to structure the scene container with a dark background and gold border so the GM narration feels like reading by torchlight
    st.subheader("The Dungeon Speaks.")
    st.write(st.session_state.current_scene)

    st.write("What do you do?")

#Asked AI help with the suggestions and how to implement and work with the in enumerate portion of the code itself and partially of many relevant parts.
    for i, action in enumerate(st.session_state.current_actions):
        if st.button(f"{i+1}. {action}", key=f"action_{i}"):
            player_message = {"role": "user", "content": f"I choose: {action}"}
            st.session_state.chat_history.append(player_message)

            raw = generatetopic(st.session_state.character_name, st.session_state.chat_history)  # fixed: was calling gmresponse1
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

    # if actions are missing but the player is still alive, show a retry button
    if not st.session_state.current_actions and st.session_state.hp > 0:
        st.warning("The dungeon lost its words. Try again.")
        if st.button("Continue"):
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