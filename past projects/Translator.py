"""
Streamlit Project 1: Translator Application

What this app does (SPECIFIC):
- Takes 1 sentence (or a short phrase) from the user and translates it into one or more target languages
  using the OpenAI Chat Completions API.

Expected user input:
- One sentence or short phrase in ANY language (English, Spanish, French, Chinese, Japanese, etc.).
"""

import os
import streamlit as st
from openai import OpenAI

# ----------------------------
# App Setup / UI
# ----------------------------
st.set_page_config(page_title="Translator App", page_icon="🌍", layout="centered")
st.title("🌍 Translator Application")
st.caption("Enter one sentence (or short phrase) and translate it into multiple languages.")

# ----------------------------
# API Key Handling (safe)
# ----------------------------
# Option A (recommended): Streamlit Secrets
# Put this in .streamlit/secrets.toml:
# OPENAI_API_KEY="your_key_here"
api_key = st.secrets.get("OPENAI_API_KEY", None)

# Option B: Environment variable
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("Missing API key. Add OPENAI_API_KEY to Streamlit Secrets or your environment variables.")
    st.stop()

client = OpenAI(api_key=api_key)

# ----------------------------
# Language Options
# ----------------------------
INPUT_LANGUAGE_OPTIONS = [
    "Auto-detect",
    "English",
    "Spanish",
    "French",
    "Mandarin Chinese",
    "Japanese",
]

OUTPUT_LANGUAGE_OPTIONS = [
    "Spanish",
    "French",
    "Mandarin Chinese",
    "Japanese",
    "English",
    "Korean",
    "German",
    "Italian",
]

# ----------------------------
# Controls (requirements)
# - 1 required text input
# - 1 Generate button
# - Streamlit component for input language setting (dropdown)
# - Streamlit component for output language selection (multiselect)
# ----------------------------
with st.container(border=True):
    input_lang = st.selectbox("Input language (optional)", INPUT_LANGUAGE_OPTIONS, index=0)

    user_text = st.text_area(
        "Text to translate (required)",
        placeholder="Type one sentence here...",
        height=110,
    )

    output_langs = st.multiselect(
        "Output language(s) (required)",
        OUTPUT_LANGUAGE_OPTIONS,
        default=["Spanish", "French", "Mandarin Chinese", "Japanese"],
    )

    generate = st.button("Generate", type="primary")

# ----------------------------
# Data Validation (NEW requirement)
# - Check required inputs not empty
# - Prevent API call if missing
# - Show warning in Streamlit
# ----------------------------
if generate:
    if not user_text or user_text.strip() == "":
        st.warning("Please enter text to translate (the text box cannot be empty).")
        st.stop()

    if not output_langs:
        st.warning("Please select at least one output language.")
        st.stop()

    # ----------------------------
    # Build the system prompt dynamically (based on output selections)
    # ----------------------------
    # If user picked an input language, we tell the model; otherwise auto-detect.
    input_lang_line = (
        f"The user says the input language is: {input_lang}."
        if input_lang != "Auto-detect"
        else "Detect the input language automatically."
    )

    langs_list = "\n".join([f"- {lang}" for lang in output_langs])

    system_prompt = f"""
You are a professional translator.
{input_lang_line}

Translate the user's text into the following languages:
{langs_list}

Return the response in this exact format (same order as selected languages):

<LANGUAGE 1>:
<translation>

<LANGUAGE 2>:
<translation>

...
"""

    # ----------------------------
    # API Call + Output
    # ----------------------------
    with st.spinner("Translating..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": user_text.strip()},
                ],
            )

            result = response.choices[0].message.content

        except Exception as e:
            st.error(f"Something went wrong calling the API: {e}")
            st.stop()

    st.subheader("✅ Translations")
    st.write(result)

    st.divider()
    st.caption("To translate again, edit your text/languages and click **Generate**.")