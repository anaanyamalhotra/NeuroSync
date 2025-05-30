import streamlit as st
import requests

st.set_page_config(page_title="NeuroSync Reflection", page_icon="🧠")

def main():
    st.title("🪞 Reflection Journal")
    st.markdown("Let NeuroSync help you process your thoughts with AI-powered journaling ✨")

    # Load session
    twin_data = st.session_state.get("twin_data")
    journal = st.session_state.get("journal_entry")

    with st.form("reflection_form"):
        name = st.text_input("What's your name?")
        email = st.text_input("Email address")
        job_title = st.text_input("Your job title")
        company = st.text_input("Company/Institution")
        current_emotion = st.text_area("How are you feeling right now?")
        recent_events = st.text_area("What happened today or recently?")
        goals = st.text_area("What are your current goals or intentions?")
        scent_note = st.text_input("Favorite perfume/cologne/candle")
        childhood_scent = st.text_area("Describe a scent from childhood you associate with something positive")
        
        submitted = st.form_submit_button("🧠 Generate Reflection")

    if submitted:
        st.info("Creating your cognitive twin...")
        try:
            twin_payload = {
                "name": name,
                "email": email,
                "job_title": job_title,
                "company": company,
                "career_goals": goals,
                "productivity_limiters": recent_events,
                "scent_note": scent_note,
                "childhood_scent": childhood_scent
            }

            twin_response = requests.post("https://cogniscent-backend-ygrv.onrender.com/generate", json=twin_payload)

            if twin_response.status_code == 200:
                twin_data = twin_response.json()
                st.session_state["twin_data"] = twin_data
                st.success("🧠 Cognitive Twin loaded.")

                st.info("Generating your personalized reflection...")

                reflect_payload = {
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

                reflect_response = requests.post("https://cogniscent-backend-ygrv.onrender.com/reflect", json=reflect_payload)

                if reflect_response.status_code == 200:
                    journal = reflect_response.json().get("journal_entry", "🧠 I couldn't generate a reflection.")
                    st.session_state["journal_entry"] = journal
                    st.success("Here's your reflection:")
                    st.markdown(f"💭 *{journal}*")
                else:
                    st.error("Failed to generate reflection.")
                    st.text(reflect_response.text)

            else:
                st.error("Failed to generate cognitive twin.")
                st.text(twin_response.text)

        except Exception as e:
            st.error(f"Request error: {e}")

    # Display last reflection if exists
    elif journal:
        st.markdown("💭 *Your last reflection:*")
        st.markdown(f"*{journal}*")

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


