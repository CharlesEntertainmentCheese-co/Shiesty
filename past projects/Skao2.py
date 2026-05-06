import streamlit as st

st.set_page_config(page_title="Simple Streamlit Website", layout="wide")

st.markdown(
    """
    <style>
      /* Page background */
      .stApp {
        background: radial-gradient(1200px 600px at 30% 0%, #0f141b 0%, #0b0f14 55%, #070a0e 100%);
        color: #eef2f7;
      }

      /* Make the main title big like the screenshot */
      h1 {
        font-size: 4rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        margin-bottom: 0.25rem !important;
      }

      /* Section header */
      .section-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
      }

      /* Border + padding around the form (this is the "card") */
      div[data-testid="stForm"] {
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 14px;
        padding: 18px 18px 10px 18px;
        background: rgba(255,255,255,0.02);
        box-shadow: 0 0 0 1px rgba(255,255,255,0.03) inset;
      }

      /* Inputs: darker fill */
      .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 12px !important;
      }

      /* Button styling (Generate) */
      .stButton > button {
        border-radius: 12px !important;
        padding: 0.7rem 1.1rem !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        background: rgba(255,255,255,0.05) !important;
      }
      .stButton > button:hover {
        border-color: rgba(255,255,255,0.30) !important;
        background: rgba(255,255,255,0.08) !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Simple Streamlit Website")
st.markdown('<div class="section-title">User Input Section</div>', unsafe_allow_html=True)

with st.form("user_inputs", clear_on_submit=False):
    name = st.text_input("Enter your name")
    bio = st.text_area("Describe your project idea")
    color = st.selectbox(
        "Choose project type",
        ["Game", "Email Generator", "Translate", "Wiki", "AI Debate"],
    )
    submitted = st.form_submit_button("Generate")

if submitted:
    if not name or not bio or not color:
        st.error("Please fill in all fields.")
    else:
        st.toast("Generated!")
        st.success("Success!")
        st.write("Name:", name)
        st.write("Idea:", bio)
        st.write("Type:", color)

st.caption("Progress")

value = st.slider("Pick a number", 0, 100, key="slider1")
st.progress(value)

if st.button("Click me"):
    st.write("You Clicked me!")