import streamlit as st

st.title("Ancient Greek Mythology Wiki")
st.info("Select a page from the sidebar to start reading.")

with st.sidebar:
	st.header("Pages")
	btn1 = st.button("Zeus", use_container_width=True)
	btn2 = st.button("Athena", use_container_width=True)
	btn3 = st.button("The Underworld", use_container_width=True)
	btn4 = st.button("The Olympians", use_container_width=True)
	btn5 = st.button("The Trojan War", use_container_width=True)
	
if btn1 == True:
    st.divider()
    st.title("Zeus")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.header("History")
        st.text("Zeus is the king of the Olympian gods and ruler of Mount Olympus. He overthrew his father Cronus and divided the world among his brothers.")
        st.header("Characteristics")
        st.text("God of the sky and thunder. Known for wielding a lightning bolt. Often depicted as a powerful bearded man.")
    with col2:
        st.header("Trivia")
        st.text("1. His Roman equivalent is Jupiter.")
        st.text("2. He had over 100 children.")
        st.text("3. His symbol is the eagle.")

if btn2 == True:
    st.divider()
    st.title("Athena")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.header("History")
        st.text("Athena is the goddess of wisdom and war strategy. She was born fully armored from the forehead of Zeus.")
        st.header("Characteristics")
        st.text("Known for intelligence over brute strength. Patron goddess of Athens. Often shown with an owl and olive branch.")
    with col2:
        st.header("Trivia")
        st.text("1. Her Roman equivalent is Minerva.")
        st.text("2. She never had a romantic partner.")
        st.text("3. She gifted the olive tree to Athens.")

if btn3 == True:
    st.divider()
    st.title("The Underworld")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.header("History")
        st.text("The Underworld is the realm of the dead ruled by Hades. Souls travel there after death guided by Hermes.")
        st.header("Characteristics")
        st.text("Divided into regions like Elysium and Tartarus. Surrounded by rivers including the Styx and Lethe.")
    with col2:
        st.header("Trivia")
        st.text("1. The three-headed dog Cerberus guards the entrance.")
        st.text("2. Only a few heroes ever escaped alive.")
        st.text("3. Charon ferries souls across the Styx.")

if btn4 == True:
    st.divider()
    st.title("The Olympians")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.header("History")
        st.text("The Twelve Olympians are the major gods who reside on Mount Olympus. They rose to power after defeating the Titans.")
        st.header("Characteristics")
        st.text("Each controls a domain of life. They interact with mortals frequently and often quarrel among themselves.")
    with col2:
        st.header("Trivia")
        st.text("1. There are actually 14 gods sometimes listed.")
        st.text("2. They drink nectar and eat ambrosia.")
        st.text("3. Mount Olympus is the highest peak in Greece.")

if btn5 == True:
    st.divider()
    st.title("The Trojan War")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.header("History")
        st.text("The Trojan War was a legendary conflict between Greece and Troy. It began after Paris of Troy took Helen from her husband Menelaus.")
        st.header("Characteristics")
        st.text("Lasted ten years. Involved gods taking sides. Ended with the famous Trojan Horse trick.")
    with col2:
        st.header("Trivia")
        st.text("1. Homer's Iliad covers part of the war.")
        st.text("2. Troy is believed to be in modern-day Turkey.")
        st.text("3. Achilles was the greatest Greek warrior.")