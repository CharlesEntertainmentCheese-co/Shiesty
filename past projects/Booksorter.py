import streamlit as st

# st.sidebar = books

books = {
    "Fantasy": {
        "Short": ("The Hobbit", "A hobbit goes on an unexpected adventure."),
        "Long": ("The Name of the Wind", "A legendary wizard recounts his life story.")
    },
    "Sci-Fi": {
        "Short": ("Fahrenheit 451", "A dystopia where books are burned."),
        "Long": ("Dune", "An epic sci-fi saga about power and survival.")
    },
    "Mystery": {
        "Short": ("The Girl with the Dragon Tattoo", "A journalist investigates a cold case."),
        "Long": ("Gone Girl", "A woman disappears and nothing is as it seems.")
    }
}



st.title("Book Recommender")
with st.sidebar:
    gen = st.selectbox("Genre", ["Fantasy", "Sci-Fi", "Mystery"])
    len = st.radio("Book Length", ["Short", "Long"], key="length")

col1, col2 = st.columns(2)
with col1:
    st.subheader(books[gen][len][0])
with col2:
    st.write(books[gen][len][1])



