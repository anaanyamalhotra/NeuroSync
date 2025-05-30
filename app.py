import streamlit as st
import importlib

st.set_page_config(page_title="NeuroSync", layout="wide")

# Map sidebar titles to file/module names (without .py)
PAGES = {
    "🏠 Home": "home",
    "🧬 Visualize NeuroProfile": "visualize_profile",
    "🪞 Reflection Journal": "reflection"
}

# Sidebar navigation
st.sidebar.title("🧠 NeuroSync Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))


module = importlib.import_module(PAGES[selection])
module.main()
