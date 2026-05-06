import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# This application runs an AI debate between two debaters with different personalities.
# The expected user input is one debate topic entered into the text box.

if "debate_log" not in st.session_state:
    st.session_state.debate_log = []

if "debate_started" not in st.session_state:
    st.session_state.debate_started = False

if "debate_topic" not in st.session_state:
    st.session_state.debate_topic = ""

st.title("Debate Arena")
st.header("2 debaters, 1 topic. Just like that video")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Debater 1: Subject A")
    st.write("Style: Attempts to Aggravate the opponent, No-filter, Emotionally Driven")
    st.write("Personality: Very Pissed-off, Aggressive, Very Offensively Focused")

with col2:
    st.subheader("Debater 2: Subject B")
    st.write("Style: Excessively Stern, Heavily Logical, Logic and Facts")
    st.write("Personality: Practically Emotionless, Apathetic, Cold")

topic = st.text_input("Enter a debate topic:")

def get_debate_response(debater_name, debater_style, topic, history, instruction):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are {debater_name}, an AI debater. "
                    f"Your debate style is {debater_style}. "
                    f"You are debating the topic: {topic}. "
                    f"Stay in character and keep your response clear and not too long."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Debate history so far:{history}"
                    f"Your task: {instruction}"
                )
            }
        ]
    )
    return response.choices[0].message.content

if st.button("Start Debate"):
    if topic == "":
        st.warning("Please enter a debate topic first.")
    else:
        st.session_state.debate_log = []
        st.session_state.debate_started = True
        st.session_state.debate_topic = topic

        history_text = ""

        debate_sections = [
            ("Opening Statements", "Give your opening statement."),
            ("Round 1", "Give your first rebuttal."),
            ("Round 2", "Give your second rebuttal."),
            ("Round 3", "Give your third rebuttal."),
            ("Closing Statements", "Give your closing statement.")
        ]

        for section_name, instruction in debate_sections:
            st.session_state.debate_log.append({
                "type": "section",
                "label": section_name
            })

            A_response = get_debate_response(
                "Subject A",
                "Attempts to Aggravate the opponent, No-filter, Emotionally Driven",
                topic,
                history_text,
                instruction
            )

            st.session_state.debate_log.append({
                "type": "message",
                "speaker": "Subject A",
                "content": A_response
            })

            history_text += f"\nAlex: {A_response}"

            B_response = get_debate_response(
                "Subject B",
                "Excessively Stern, Heavily Logical, Logic and Facts",
                topic,
                history_text,
                instruction
            )

            st.session_state.debate_log.append({
                "type": "message",
                "speaker": "Subject B",
                "content": B_response
            })

            history_text += f"\nBlaze: {B_response}"

st.subheader("Debate Log")

if st.session_state.debate_log:
    current_section = None
    section_messages = []

    for item in st.session_state.debate_log:
        if item["type"] == "section":
            if current_section is not None:
                with st.expander(current_section):
                    for message in section_messages:
                        with st.chat_message(message["speaker"]):
                            st.write(message["content"])

            current_section = item["label"]
            section_messages = []

        elif item["type"] == "message":
            section_messages.append(item)

    if current_section is not None:
        with st.expander(current_section):
            for message in section_messages:
                with st.chat_message(message["speaker"]):
                    st.write(message["content"])
else:
    st.write("No debate has been generated yet.")