import streamlit as st

def main():
    st.set_page_config(page_title="NeuroSync 🧠", layout="centered")
    st.title("Welcome to NeuroSync 🧠")

    st.markdown("""
    **NeuroSync** is your interactive Cognitive Twin Intelligence platform — powered by neuroscience, olfactory memory, and emotional AI.

    ### 🌟 What You Can Do:
    - 🧬 **Generate Your Cognitive Twin**: Based on scent preferences, career goals, and stress patterns
    - 🎮 **Get Xbox Game Recommendations**: Curated using your dominant neurotransmitter profile
    - 🎧 **Explore Spotify Playlists**: Tailored to your mood and brain chemistry
    - 📓 **Journal with GPT-4**: Reflect on your emotional state using AI-guided insights
    - 🧠 **Visualize Your Brain**: See how your amygdala, hippocampus, and hypothalamus respond

    ### 🧠 How It Works:
    We analyze your responses across 7 personalized questions, including:
    - Childhood scent memories
    - Favorite perfumes and stressors
    - Career aspirations and daily habits

    These are translated into:
    - A 5-point neurotransmitter map: `dopamine`, `serotonin`, `GABA`, `oxytocin`, `cortisol`
    - Brain region sub-vectors
    - Personalized Xbox + music suggestions
    - A reflection-ready mood profile

    ---
    👉 Use the **sidebar tabs** to:
    - 🧬 Generate or explore your twin under **NeuroProfile Generator**
    - 📓 Reflect in **NeuroJournal Reflection**
    - 📊 Dive into brain chemistry in **Twin Explorer**

    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
