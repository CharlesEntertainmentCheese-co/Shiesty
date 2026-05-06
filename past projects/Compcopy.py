import streamlit as st
import time

with st.status("Running tasks...", expanded=True) as status:
    st.write("Step 1...")
    bar = st.progress(0)
    for i in range(100):
        bar.progress(i+1)
        time.sleep(0.01)
    st.update(label="Complete", state="complete")
