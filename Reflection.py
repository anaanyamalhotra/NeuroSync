import streamlit as st
import requests

def main():
    st.title("🪞 Reflection Journal")
    st.markdown("Let NeuroSync help you process your thoughts with AI-powered journaling ✨")

    name = st.text_input("What's your name?")
    current_emotion = st.text_area("How are you feeling right now?")
    recent_events = st.text_area("What happened today or recently?")
    goals = st.text_area("What are your current goals or intentions?")

    if st.button("Generate Reflection"):
        if not name or not current_emotion or not recent_events or not goals:
            st.warning("Please fill in all fields to get a meaningful reflection.")
        else:
            with st.spinner("Reflecting..."):
                try:
                    response = requests.post(
                        "https://cogniscent-backend-ygrv.onrender.com/reflect",
                        json={
                            "name": name,
                            "current_emotion": current_emotion,
                            "recent_events": recent_events,
                            "goals": goals
                        }
                    )
                    if response.status_code == 200:
                        journal = response.json().get("journal_entry", "")
                        st.success("Here's your reflection:")
                        st.markdown(f"💭 *{journal}*")
                    else:
                        st.error("Something went wrong. Please try again.")
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
