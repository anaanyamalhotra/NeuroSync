import streamlit as st
import requests
import datetime


def main():
    st.title("🪞 Reflection Journal")
    st.markdown("Let NeuroSync help you process your thoughts with AI-powered journaling ✨")

    # Load prior twin
    twin_data = st.session_state.get("profile")
    journal_history = st.session_state.get("journal_history", [])

    if not twin_data:
        st.warning("⚠️ Please generate your NeuroProfile first in the previous tab.")
        return

    with st.form("reflection_form"):
        name = twin_data["name"]
        st.markdown(f"**Name:** {name}")
        current_emotion = st.text_area("How are you feeling right now?")
        recent_events = st.text_area("What happened today or recently?")
        goals = st.text_area("What are your current goals or intentions?")
        submitted = st.form_submit_button("🧠 Generate Reflection")

    if submitted:
        st.info("Analyzing neurotransmitters and generating reflection...")

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

        try:
            res = requests.post("https://cogniscent-backend-ygrv.onrender.com/reflect", json=reflect_payload)
            res.raise_for_status()
            journal = res.json().get("journal_entry", "🧠 I couldn't generate a reflection.")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"[{timestamp}]\n{journal}"
            journal_history.append(entry)
            st.session_state["journal_history"] = journal_history
            st.success("Here's your reflection:")
            st.markdown(f"💭 *{journal}*")

            st.download_button(
                label="📥 Download Reflection",
                data=entry,
                file_name=f"{name.replace(' ', '_')}_reflection.txt",
                mime="text/plain"
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")


    # Show history
    if journal_history:
        st.markdown("## 🧾 Past Reflections")
        for j in reversed(journal_history):
            st.markdown("---")
            st.markdown(j.replace("\n", "\n\n"))

if __name__ == "__main__":
    main()



