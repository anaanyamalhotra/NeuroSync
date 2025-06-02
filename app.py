import streamlit as st
import importlib

st.set_page_config(page_title="NeuroSync", layout="wide")


PAGES = {
    "🏠 Home": "home",
    "🧬 Visualize NeuroProfile": "Visualize_Profile",
    "📚 Twin Explorer": "Twin_Explorer"
    
}


st.sidebar.title("🧠 NeuroSync Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))


module = importlib.import_module(PAGES[selection])
module.main()
