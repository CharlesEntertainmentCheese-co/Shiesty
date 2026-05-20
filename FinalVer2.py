import streamlit as st
from openai import OpenAI
import json
import re

# -------------------------
# Page Config (must be first)
# -------------------------
st.set_page_config(
    page_title="Pure Rap Checker",
    page_icon=None,
    layout="centered"
)

# -------------------------
# HIP-HOP THEME INJECTION
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@400;600;700&family=Share+Tech+Mono&display=swap');

/* ===== ROOT VARIABLES ===== */
:root {
    --gold:        #FFD700;
    --gold-dim:    #B8960C;
    --red:         #E8132B;
    --white:       #F0EDE4;
    --off-white:   #C8C3B5;
    --bg:          #0A0A0A;
    --bg2:         #111111;
    --bg3:         #1A1A1A;
    --border:      #2A2A2A;
    --chain:       #8B7536;
}

/* ===== GLOBAL RESET ===== */
html, body, [class*="css"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--white) !important;
}

/* ===== BACKGROUND — graffiti-wall texture via noise ===== */
.stApp {
    background-color: var(--bg) !important;
    background-image:
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(255,215,0,0.015) 2px,
            rgba(255,215,0,0.015) 4px
        ),
        radial-gradient(ellipse at 20% 10%, rgba(232,19,43,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 90%, rgba(255,215,0,0.06) 0%, transparent 50%);
    background-attachment: fixed;
}



/* ===== MAIN CONTAINER ===== */
.block-container {
    max-width: 780px !important;
    padding: 2rem 2rem 4rem !important;
}

/* ===== TITLE ===== */
h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 4rem !important;
    letter-spacing: 0.12em !important;
    background: linear-gradient(135deg, var(--gold) 0%, #FFF5A0 40%, var(--gold-dim) 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-shadow: none !important;
    line-height: 1 !important;
    margin-bottom: 0.2rem !important;
}

/* ===== SUBHEADERS ===== */
h2, h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 0.08em !important;
    color: var(--gold) !important;
    text-transform: uppercase !important;
    border-bottom: 2px solid var(--border) !important;
    padding-bottom: 0.3rem !important;
}

h3 {
    font-size: 1.6rem !important;
    color: var(--white) !important;
    border-bottom-color: var(--gold-dim) !important;
}

/* ===== BODY TEXT ===== */
p, li, span, label, .stMarkdown {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.1rem !important;
    color: var(--off-white) !important;
    letter-spacing: 0.03em !important;
}

/* ===== DIVIDER ===== */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
    position: relative !important;
}
hr::after {
    content: '✦';
    position: absolute;
    top: -0.6rem;
    left: 50%;
    transform: translateX(-50%);
    color: var(--gold);
    font-size: 0.7rem;
    background: var(--bg);
    padding: 0 0.4rem;
}

/* ===== BUTTONS ===== */
.stButton > button {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.3rem !important;
    letter-spacing: 0.15em !important;
    background: linear-gradient(135deg, var(--gold-dim), var(--gold)) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 0.55rem 2rem !important;
    text-transform: uppercase !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 4px 20px rgba(255,215,0,0.25), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--gold), #FFED80) !important;
    box-shadow: 0 6px 28px rgba(255,215,0,0.45) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
    box-shadow: 0 2px 10px rgba(255,215,0,0.3) !important;
}

/* ===== INPUT FIELDS ===== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem !important;
    background: var(--bg3) !important;
    color: var(--gold) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    padding: 0.75rem 1rem !important;
    caret-color: var(--gold) !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold-dim) !important;
    box-shadow: 0 0 0 1px var(--gold-dim), 0 0 12px rgba(255,215,0,0.1) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #444 !important;
}

/* ===== SELECT BOX ===== */
.stSelectbox > div > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    color: var(--white) !important;
}
.stSelectbox > div > div:hover {
    border-color: var(--gold-dim) !important;
}

/* ===== METRICS ===== */
[data-testid="stMetric"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    padding: 0.8rem 1rem !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--gold);
}
[data-testid="stMetricLabel"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
    color: var(--off-white) !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2.2rem !important;
    color: var(--gold) !important;
}

/* ===== PROGRESS BAR ===== */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--red), #FF6B1A) !important;
    border-radius: 0 !important;
    transition: width 0.5s ease !important;
}
.stProgress > div > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    height: 14px !important;
}

/* ===== CHAT MESSAGES ===== */
[data-testid="stChatMessage"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    padding: 0.8rem 1rem !important;
    margin-bottom: 0.5rem !important;
}
/* User bars — gold left-border */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-left: 3px solid var(--gold) !important;
    background: rgba(255,215,0,0.04) !important;
}
/* AI bars — red left-border */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-left: 3px solid var(--red) !important;
    background: rgba(232,19,43,0.04) !important;
}

/* ===== ALERTS / WARNINGS / SUCCESS / ERROR ===== */
.stAlert {
    border-radius: 2px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.03em !important;
}
div[data-testid="stAlert"][data-baseweb="notification"] {
    background: rgba(232,19,43,0.12) !important;
    border: 1px solid var(--red) !important;
    color: var(--white) !important;
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.1em !important;
    color: var(--gold) !important;
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
}
.streamlit-expanderContent {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
}

/* ===== SPINNER ===== */
.stSpinner > div {
    border-color: var(--gold) transparent transparent transparent !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 0; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* ===== COLUMNS ===== */
[data-testid="column"] {
    padding: 0.25rem !important;
}

/* ===== DECORATIVE HEADER STRIP ===== */
.rap-header-strip {
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg,
        var(--red) 0%, var(--red) 33%,
        var(--gold) 33%, var(--gold) 66%,
        var(--red) 66%, var(--red) 100%
    );
    margin-bottom: 1.5rem;
}

/* ===== BATTLE BANNER ===== */
.battle-banner {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    letter-spacing: 0.2em;
    color: var(--red);
    text-align: center;
    padding: 0.25rem 0;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    margin: 0.5rem 0 1.5rem;
}

/* ===== VS BADGE ===== */
.vs-badge {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    color: var(--red);
    text-align: center;
    letter-spacing: 0.1em;
}

/* ===== CHAIN DECORATION ===== */
.chain-divider {
    text-align: center;
    font-size: 1.2rem;
    color: var(--chain);
    letter-spacing: 0.3em;
    margin: 0.5rem 0;
    opacity: 0.7;
}

/* ===== JUDGEMENT CARD ===== */
.judgement-card {
    background: var(--bg3);
    border: 1px solid var(--gold-dim);
    border-radius: 2px;
    padding: 1rem 1.2rem;
    margin-top: 0.5rem;
    position: relative;
    overflow: hidden;
}
.judgement-card::before {
    content: '★ JUDGEMENT SERVED ★';
    position: absolute;
    top: 0; left: 0; right: 0;
    background: var(--gold);
    color: #000;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-align: center;
    padding: 0.15rem 0;
}
</style>

<!-- Header decoration -->
<div class="rap-header-strip"></div>
""", unsafe_allow_html=True)


# -------------------------
# OpenAI Client
# -------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Pure Rap Checker")

st.markdown('<div class="chain-divider">- - - - - - - - - - -</div>', unsafe_allow_html=True)
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
# Safety Filter
# -------------------------
def check_bar_with_tsa(text):
    tsa_system_prompt = """
You are TSA Bot, a strict content screener for a rap battle game.
Your ONLY job is to check if the submitted text contains prohibited content.
Respond ONLY in valid JSON: {"allowed": true/false, "reason": "..."}
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
# System Prompt
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
# API Call
# -------------------------
def generate_judgement(aka, difficulty, user_bar):
    messages = [{"role": "system", "content": get_system_prompt(aka, difficulty)}]
    messages += st.session_state.battle_history[-10:]
    messages.append({"role": "user", "content": f"My rap bar: {user_bar}"})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    raw = response.choices[0].message.content
    try:
        result = json.loads(raw)
    except Exception:
        result = {
            "score": 50,
            "feedback": "The AI response broke format, but your bar was received. Try again with a cleaner line.",
            "hp_deduction": 25,
            "ai_bar": "Your format got lucky, but your flow still like an oldie on a wheelchair — crippled, trash and junk like a backup that got backfilled."
        }
    return result


# -------------------------
# Restart
# -------------------------
def restart_game():
    st.session_state.begin_judging = False
    st.session_state.rapper_aka = ""
    st.session_state.difficulty = "Medium"
    st.session_state.player_hp = 100
    st.session_state.ai_hp = 100
    st.session_state.battle_history = []
    st.session_state.last_result = None


# ======================================================
# START SCREEN
# ======================================================
if not st.session_state.begin_judging:

    st.markdown('<div class="battle-banner">STEP UP OR STEP ASIDE</div>', unsafe_allow_html=True)
    st.subheader("Fall to either rags or riches. Your bars decide your fate.")

    aka_input = st.text_input(
        "Enter your rapper AKA:",
        placeholder="e.g. Lil Shiesty"
    )

    difficulty_input = st.selectbox(
        "Choose battle difficulty:",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("ENTER THE RING"):
        if aka_input.strip() == "":
            st.warning("Missing an AKA. What's a rapper without a name? A fool frfr gng.")
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


# ======================================================
# BATTLE SCREEN
# ======================================================
else:
    # VS Header
    col_l, col_vs, col_r = st.columns([5, 2, 5])
    with col_l:
        st.markdown(f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#FFD700;letter-spacing:0.1em;text-align:right;'>{st.session_state.rapper_aka}</div>", unsafe_allow_html=True)
    with col_vs:
        st.markdown("<div class='vs-badge'>VS</div>", unsafe_allow_html=True)
    with col_r:
        st.markdown("<div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#E8132B;letter-spacing:0.1em;'>JUDGEBOT</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center;font-family:Barlow Condensed,sans-serif;font-size:0.9rem;color:#555;letter-spacing:0.2em;text-transform:uppercase;'>Difficulty: {st.session_state.difficulty}</div>", unsafe_allow_html=True)
    st.markdown('<div class="chain-divider">- - - - - - - - - - -</div>', unsafe_allow_html=True)

    # HP Bars
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='font-family:Bebas Neue,sans-serif;letter-spacing:0.1em;color:#FFD700;'>YOUR HP</div>", unsafe_allow_html=True)
        st.progress(st.session_state.player_hp / 100)
        st.metric("Player HP", st.session_state.player_hp)

    with col2:
        st.markdown("<div style='font-family:Bebas Neue,sans-serif;letter-spacing:0.1em;color:#E8132B;'>JUDGEBOT HP</div>", unsafe_allow_html=True)
        st.progress(st.session_state.ai_hp / 100)
        st.metric("AI HP", st.session_state.ai_hp)

    st.divider()

    # Battle Chat
    st.subheader("Battle Chat")

    for msg in st.session_state.battle_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])

    st.divider()

    # Game Over
    if st.session_state.player_hp <= 0:
        st.markdown('<div class="battle-banner">YOU GOT BODIED — GAME OVER</div>', unsafe_allow_html=True)
        st.error("You lost the battle. Judgebot cooked your street cred.")
        if st.button("RESTART BATTLE"):
            restart_game()
            st.rerun()

    elif st.session_state.ai_hp <= 0:
        st.markdown('<div class="battle-banner" style="color:#FFD700;">JUDGEBOT GOT BODIED — YOU WIN</div>', unsafe_allow_html=True)
        st.success("You won the battle. Judgebot got bodied.")
        if st.button("RESTART BATTLE"):
            restart_game()
            st.rerun()

    else:
        user_bar = st.text_area(
            "Spit your bars:",
            placeholder="Drop your hardest line here...",
            height=120
        )

        if st.button("SPIT IT"):
            if user_bar.strip() == "":
                st.warning("Silence doesn't win battles, cuh.")
            else:
                with st.spinner("TSA Bot is checking your bar..."):
                    is_blocked, block_reason = check_bar_with_tsa(user_bar)

                if is_blocked:
                    st.warning(f"Bar blocked by TSA Bot: {block_reason} — Rewrite and try again.")
                else:
                    with st.spinner("Judgebot is judging your bars..."):
                        result = generate_judgement(
                            st.session_state.rapper_aka,
                            st.session_state.difficulty,
                            user_bar
                        )

                    score        = max(0, min(int(result.get("score", 50)), 100))
                    feedback     = result.get("feedback", "No feedback given.")
                    hp_deduction = max(5, min(int(result.get("hp_deduction", 10)), 40))
                    ai_bar       = result.get("ai_bar", "I would respond, but your bar already defeated itself.")

                    ai_damage = max(5, round(score / 3))

                    st.session_state.ai_hp     = max(0, st.session_state.ai_hp - ai_damage)
                    st.session_state.player_hp = max(0, st.session_state.player_hp - hp_deduction)

                    st.session_state.battle_history.append({"role": "user",      "content": user_bar})
                    st.session_state.battle_history.append({"role": "assistant", "content": ai_bar})

                    st.session_state.last_result = {
                        "score":        score,
                        "feedback":     feedback,
                        "hp_deduction": hp_deduction,
                        "ai_damage":    ai_damage
                    }

                    st.rerun()

    # ===== JUDGEMENT RESULTS =====
    if st.session_state.last_result:
        st.divider()
        st.markdown('<div class="judgement-card" style="padding-top:1.8rem;">', unsafe_allow_html=True)

        result_col1, result_col2 = st.columns(2)
        with result_col1:
            st.metric("Your Score",      st.session_state.last_result["score"])
            st.metric("Damage You Took", st.session_state.last_result["hp_deduction"])
            st.metric("Damage You Dealt",st.session_state.last_result["ai_damage"])
        with result_col2:
            st.markdown("<div style='font-family:Bebas Neue,sans-serif;letter-spacing:0.1em;color:#FFD700;font-size:1rem;'>FEEDBACK</div>", unsafe_allow_html=True)
            st.write(st.session_state.last_result["feedback"])

        st.markdown('</div>', unsafe_allow_html=True)

    # ===== FULL HISTORY =====
    with st.expander("VIEW FULL BATTLE HISTORY"):
        for i, msg in enumerate(st.session_state.battle_history, start=1):
            role_label = "YOU" if msg["role"] == "user" else "JUDGEBOT"
            color = "#FFD700" if msg["role"] == "user" else "#E8132B"
            st.markdown(
                f"<div style='margin-bottom:0.5rem;'>"
                f"<span style='font-family:Bebas Neue,sans-serif;color:{color};letter-spacing:0.1em;font-size:0.9rem;'>{i}. {role_label}</span>"
                f"<br><span style='font-family:Share Tech Mono,monospace;font-size:0.9rem;color:#C8C3B5;'>{msg['content']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.divider()

    if st.button("RESTART BATTLE"):
        restart_game()
        st.rerun()

