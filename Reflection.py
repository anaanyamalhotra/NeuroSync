import streamlit as st
import requests

st.set_page_config(page_title="NeuroSync Reflection", page_icon="🧠")

def main():
    st.title("🪞 Reflection Journal")
    st.markdown("Let NeuroSync help you process your thoughts with AI-powered journaling ✨")

    with st.form("reflection_form"):
        name = st.text_input("What's your name?")
        current_emotion = st.text_area("How are you feeling right now?")
        recent_events = st.text_area("What happened today or recently?")
        goals = st.text_area("What are your current goals or intentions?")
        st.form_submit_button("Generate Reflection")

    # Automatically fetch profile based on name
    twin_data = st.session_state.get("twin_data")

    if st.button("📬 Load Cognitive Twin"):
        st.info("Fetching your profile...")
        try:
            response = requests.post(
                "https://cogniscent-backend-ygrv.onrender.com/generate",
                json={
                    "name": name,
                    "email": "example@email.com",
                    "job_title": "student",
                    "company": "MSU",
                    "career_goals": goals,
                    "productivity_limiters": recent_events,
                    "scent_note": "lavender",  # or add input
                    "childhood_scent": "vanilla"  # or add input
                }
            )
            if response.status_code == 200:
                twin_data = response.json()
                st.session_state["twin_data"] = twin_data
                st.success("Cognitive profile loaded.")
            else:
                st.error("Failed to generate cognitive twin.")
        except Exception as e:
            st.error(f"Error: {e}")

    if twin_data and st.button("🧠 Reflect"):
        st.info("Generating your reflection...")
        try:
            response = requests.post(
                "https://cogniscent-backend-ygrv.onrender.com/reflect",
                json={
                    "name": name,
                    "current_emotion": current_emotion,
                    "recent_events": recent_events,
                    "goals": goals,
                    "neurotransmitters": twin_data["neurotransmitters"],
                    "xbox_game": twin_data["xbox_game"],
                    "game_mode": twin_data["game_mode"],
                    "duration_minutes": twin_data["duration_minutes"],
                    "switch_time": twin_data["switch_time"]
                }
            )
            if response.status_code == 200:
                journal = response.json().get("journal_entry", "🧠 I couldn't generate a reflection.")
                st.success("Here's your reflection:")
                st.markdown(f"💭 *{journal}*")
            else:
                st.error("Something went wrong during reflection.")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()

