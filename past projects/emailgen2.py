import os
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Email Generator")
#Title
st.header("Your trusty partner to make selfish demands!")
#
with st.form("creature_form"):
    st.title("Query")
    name = st.text_input("Whats your name?")
    recipient = st.text_input("Whats the recipient name?")
    style = st.text_input("Whats the style you want?")
    topic = st.text_area("Whats the email about?")
    tone = st.multiselect("Pick your tone:", ["Angry", "Sad", "Ecstatic"])
    length = st.number_input(
        "How many words do you want it to be?",
        value=0
    )

    submit = st.form_submit_button("Generate")

if submit:
    if name == "" or recipient == "" or style == "" or topic == "":
        st.warning("Please fill in all the boxes first.")
    else:
        tone_text = ", ".join(tone)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that writes emails."
                },
                {
                    "role": "user",
                    "content": f"""
Write an email for me.

My name is {name}.
The recipient is {recipient}.
The style should be {style}.
The tone should be {tone_text}.
The email is about: {topic}.
Make it around {length} words.
"""
                }
            ]
        )

        result = response.choices[0].message.content
        st.subheader("Generated Email")
        st.write(result)
#The application itself is a simple email generator, but the extension itself is a number_input which allows the user to scale or type a specific number within the box which then determines the length of the email is (EX: if its '1000' then it'll be a 1-thousand word length email)