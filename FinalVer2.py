import streamlit as st
from openai import OpenAI
import json
import re
# Import re allows the user to access a regular expression is a special sequence of characters that forms a search pattern,
# allowing you to match, search, and manipulate text with high precision.

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Pure Rap Checker 🎤")
st.write("Enter the ring, spit your bars, get judged, and survive the AI opponent.")

# -------------------------
# Session State Setup
# -------------------------
if "begin_judging" not in st.session_state:
    st.session_state.begin_judging = False

if "rapper_aka" not in st.session_state:
    st.session_state.rapper_aka = ""

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"

if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100

if "ai_hp" not in st.session_state:
    st.session_state.ai_hp = 100

if "battle_history" not in st.session_state:
    st.session_state.battle_history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# -------------------------
# Safety filter for censoring
# -------------------------
def check_bar_with_tsa(text):
    tsa_system_prompt = """
You are TSA Bot, a strict content screener for a rap battle game.
Your ONLY job is to check if the submitted text contains prohibited content.

Prohibited content includes:
- Racial slurs or hate speech targeting any ethnicity or nationality
- Sexist, homophobic, or transphobic language
- Content that targets real individuals with threats or harassment
- Sexual content involving minors
- Explicit instructions for real-world violence or harm

Rap battle content that is aggressive, boastful, or uses mild profanity is ALLOWED.
Dissing someone's rap skills, flow, or persona is ALLOWED.

Respond ONLY in valid JSON with this exact structure:
{"allowed": true, "reason": ""}
or
{"allowed": false, "reason": "Brief explanation of what was flagged"}

Do not include any other text outside the JSON.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": tsa_system_prompt},
            {"role": "user", "content": f"Screen this text: {text}"}
        ],
        max_tokens=100,
        temperature=0
    )
    raw = response.choices[0].message.content.strip()
    try:
        result = json.loads(raw)
        is_blocked = not result.get("allowed", True)
        reason = result.get("reason", "Prohibited content detected.")
        return is_blocked, reason
    except Exception:
        return True, "Content screening encountered an error. Please rephrase."

# -------------------------
# System prompt
# -------------------------
def get_system_prompt(aka, difficulty):
    return f"""
You are Judgebot, an AI rap-battle live judgement system.

The player's rapper name is {aka}.
The difficulty is {difficulty}.

Your job has 2 roles:

ROLE 1: Judge the player's rap bar.
Judge based on these criteria:
1. Rhythmic Scheme: Does the rhythm and flow feel natural or forced?
2. Wordplay: Are there metaphors, double meanings, comparisons, or clever lines?
3. Punchline Quality: Does the punchline actually hit or is it weak?
4. Battle Impact: Does the bar respond to the opponent and move the battle forward?

Give specific feedback based on the user's actual line. Do not be generic.

ROLE 2: Fire back with your own AI rap bar.
Your comeback should match the chosen difficulty.
Reference earlier lines when possible so the battle feels continuous.

Hard rules:
- No slurs.
- No racist, sexist, homophobic, or dehumanizing remarks.
- Do not insult real identity, race, gender, religion, disability, or sexuality.
- Roast only rap skill, persona, flow, weak bars, and battle performance.
- If the user uses prohibited content, do not repeat it.

Respond ONLY in valid JSON with this exact structure:

{{
  "score": 0,
  "feedback": "specific 1-2 sentence feedback",
  "hp_deduction": 10,
  "ai_bar": "AI comeback line"
}}

Score must be 0-100.
hp_deduction must be 5-40.
"""


# -------------------------
# API call
# -------------------------
def generate_judgement(aka, difficulty, user_bar):
    messages = [
        {"role": "system", "content": get_system_prompt(aka, difficulty)}
    ]

    # Only send last 10 messages so context does not get too long
    messages += st.session_state.battle_history[-10:]

    messages.append({
        "role": "user",
        "content": f"My rap bar: {user_bar}"
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    raw = response.choices[0].message.content

    try:
        result = json.loads(raw)
    except Exception:
        # Backup if AI messes up JSON
        result = {
            "score": 50,
            "feedback": "The AI response broke format, but your bar was received. Try again with a cleaner line.",
            "hp_deduction": 25,
            "ai_bar": "Your format got lucky, but your flow still like an oldie on a wheelchair crippled, trash and junk like a back-up thats got backfilled."
        }

    return result


# -------------------------
# Restart Function
# -------------------------
def restart_game():
    st.session_state.begin_judging = False
    st.session_state.rapper_aka = ""
    st.session_state.difficulty = "Medium"
    st.session_state.player_hp = 100
    st.session_state.ai_hp = 100
    st.session_state.battle_history = []
    st.session_state.last_result = None


# -------------------------
# Start Screen
# -------------------------
if not st.session_state.begin_judging:
    st.subheader("Fall to either rags or riches. Your bars decide your fate.")

    aka_input = st.text_input(
        "Enter your rapper AKA:",
        placeholder="e.g. Lil Shiesty"
    )

    difficulty_input = st.selectbox(
        "Choose battle difficulty:",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("Enter the Ring"):
        if aka_input.strip() == "":
            st.warning("Missing an AKA. What's a rapper without a name? a fool frfr gng.")
        else:
            with st.spinner("TSA Bot is checking your name..."):
                aka_blocked, aka_reason = check_bar_with_tsa(aka_input)
            if aka_blocked:
                st.warning(f"That AKA was flagged: {aka_reason}. Pick a different name.")
            else:
                st.session_state.begin_judging = True
                st.session_state.rapper_aka = aka_input.strip()
                st.session_state.difficulty = difficulty_input
                st.session_state.player_hp = 100
                st.session_state.ai_hp = 100
                st.session_state.battle_history = [
                    {
                        "role": "assistant",
                        "content": "Step in the ring if you dare — spit first, and I'll show you where your flow needs work."
                    }
                ]
                st.rerun()
#For the censor system, there are issues like when someone uses a niche slur or insult that counts as derogatory,
#but due to the rare and uncommon or rare nature of the word itself I cannot do research on the internet the entire time
#searching for niche and rare insults that count as derogatory.

# -------------------------
# Battle Screen
# -------------------------
else:
    st.subheader(f"{st.session_state.rapper_aka} vs Judgebot")
    st.write(f"Difficulty: **{st.session_state.difficulty}**")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Your HP")
        st.progress(st.session_state.player_hp / 100)
        st.metric("Player HP", st.session_state.player_hp)

    with col2:
        st.write("Judgebot HP")
        st.progress(st.session_state.ai_hp / 100)
        st.metric("AI HP", st.session_state.ai_hp)

    st.divider()

    st.subheader("Battle Chat")

    for msg in st.session_state.battle_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])

    st.divider()

    # Game Over Check
    if st.session_state.player_hp <= 0:
        st.error("You lost the battle. Judgebot cooked your street cred.")
        if st.button("Restart Battle"):
            restart_game()
            st.rerun()

    elif st.session_state.ai_hp <= 0:
        st.success("You won the battle. Judgebot got bodied.")
        if st.button("Restart Battle"):
            restart_game()
            st.rerun()

    else:
        # FIX 1: Moved generate_judgement call inside the correct branch.
        # Previously the if/else was inverted — judging ran when button was NOT
        # clicked, and the is_blocked branch called generate_judgement(...) with
        # no arguments (syntax error / wrong placeholder).
        user_bar = st.text_area(
            "Write your lyrics/bars/diss below:",
            placeholder="Spit your best bar here..."
        )

        if st.button("Spit It"):
            if user_bar.strip() == "":
                st.warning("Silence doesn't win battles, cuh.")
            else:
                with st.spinner("TSA Bot is checking your bar..."):
                    is_blocked, block_reason = check_bar_with_tsa(user_bar)

                if is_blocked:
                    st.warning(f"🚫 Bar blocked by TSA Bot: {block_reason} — Rewrite and try again.")
                else:
                    with st.spinner("Judgebot is judging your bars..."):
                        result = generate_judgement(
                            st.session_state.rapper_aka,
                            st.session_state.difficulty,
                            user_bar
                        )

                    score = int(result.get("score", 50))
                    feedback = result.get("feedback", "No feedback given.")
                    hp_deduction = int(result.get("hp_deduction", 10))
                    ai_bar = result.get("ai_bar", "I would respond, but your bar already defeated itself.")

                    # Clamp values to safe ranges
                    score = max(0, min(score, 100))
                    hp_deduction = max(5, min(hp_deduction, 40))

                    # User damages AI based on score
                    ai_damage = max(5, round(score / 3))

                    st.session_state.ai_hp -= ai_damage
                    st.session_state.player_hp -= hp_deduction

                    st.session_state.ai_hp = max(0, st.session_state.ai_hp)
                    st.session_state.player_hp = max(0, st.session_state.player_hp)

                    st.session_state.battle_history.append({
                        "role": "user",
                        "content": user_bar
                    })

                    st.session_state.battle_history.append({
                        "role": "assistant",
                        "content": ai_bar
                    })

                    st.session_state.last_result = {
                        "score": score,
                        "feedback": feedback,
                        "hp_deduction": hp_deduction,
                        "ai_damage": ai_damage
                    }

                    st.rerun()

    # FIX 2: Moved Results Section, Full Battle History expander, and Restart
    # button OUT of the `else` block so they are always visible on the battle
    # screen (including after game over), not only when HP > 0.

    # Results Section
    if st.session_state.last_result:
        st.divider()
        st.subheader("Judgement Served")

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.metric("Your Score", st.session_state.last_result["score"])
            st.metric("Damage You Took", st.session_state.last_result["hp_deduction"])
            st.metric("Damage You Dealt", st.session_state.last_result["ai_damage"])

        with result_col2:
            st.write("Feedback:")
            st.write(st.session_state.last_result["feedback"])

    with st.expander("View Full Battle History"):
        for i, msg in enumerate(st.session_state.battle_history, start=1):
            st.write(f"{i}. **{msg['role'].title()}**: {msg['content']}")

    st.divider()

    if st.session_state.player_hp > 0 and st.session_state.ai_hp > 0:
        if st.button("Restart Battle", key="restart_mid"):
            restart_game()
            st.rerun()