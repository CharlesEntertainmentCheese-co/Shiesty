import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Makes sidebar buttons full width
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Ancient Greek Mythology Wiki")
st.info("Select a page from the sidebar to start reading.")

def generate_page(topic):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You write short Greek mythology wiki pages."
            },
            {
                "role": "user",
                "content": f"""
Write a short mythology wiki page about {topic}.

Include:
History
Characteristics
Trivia (3 numbered facts)

Keep it short and clear.
"""
            }
        ]
    )
    return response.choices[0].message.content

# Run the API only once and save results in a dictionary
if "myth_dict" not in st.session_state:
    st.session_state.myth_dict = {
        "Zeus": generate_page("Zeus"),
        "Athena": generate_page("Athena"),
        "The Underworld": generate_page("The Greek Underworld"),
        "The Olympians": generate_page("The Twelve Olympian Gods"),
        "The Trojan War": generate_page("The Trojan War in Greek Mythology")
    }

with st.sidebar:
    st.header("Pages")
    btn1 = st.button("Zeus")
    btn2 = st.button("Athena")
    btn3 = st.button("The Underworld")
    btn4 = st.button("The Olympians")
    btn5 = st.button("The Trojan War")

if btn1:
    st.divider()
    st.title("Zeus")
    st.divider()
    st.write(st.session_state.myth_dict["Zeus"])

if btn2:
    st.divider()
    st.title("Athena")
    st.divider()
    st.write(st.session_state.myth_dict["Athena"])

if btn3:
    st.divider()
    st.title("The Underworld")
    st.divider()
    st.write(st.session_state.myth_dict["The Underworld"])

if btn4:
    st.divider()
    st.title("The Olympians")
    st.divider()
    st.write(st.session_state.myth_dict["The Olympians"])

if btn5:
    st.divider()
    st.title("The Trojan War")
    st.divider()
    st.write(st.session_state.myth_dict["The Trojan War"])



#Ensure The response call only runs once, the information you get out of it is saved into a dictionary variable and then accesses the dictionary whenever you click the buttons on the sidebar
#The dictionaries are linked to the sidebar buttons. 
#Make sure the website is not interactable until the information is already generated.