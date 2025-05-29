# Streamlit frontend app

import streamlit as st
import importlib

st.set_page_config(page_title="NeuroSync", layout="wide")

PAGES = {
    "🏠 Home": "Home",
    "🧬 Visualize NeuroProfile": "🧬 Visualize_Profile",
    "🪞 Reflection Journal": "🪞 Reflection"
}

st.sidebar.title("🧠 NeuroSync Navigation")

selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
module = importlib.import_module(page)
module.main()
