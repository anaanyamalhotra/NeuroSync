import streamlit as st

def main():
    st.set_page_config(page_title="NeuroSync", layout="wide")
    st.title("Welcome to NeuroSync 🧠")
    st.markdown("""
    **NeuroSync** is your personalized Cognitive Twin Intelligence platform.

    🧬 Understand your unique brain chemistry
    🎮 Get neuroscience-backed game, scent, and music recommendations
    🪞 Reflect with GPT-powered journaling

    ### 🧠 How it works:
    - We analyze your scent memory, stress triggers, routines, and personal goals
    - This creates a "neuroprofile" based on five key neurotransmitters
    - Your brain regions are mapped and interpreted for insight & feedback

    👉 Use the sidebar to begin:
    - Visualize your neuroprofile
    - Try AI journaling for reflection
    """)

if __name__ == "__main__":
    main()
