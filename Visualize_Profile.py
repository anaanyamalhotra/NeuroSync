import streamlit as st
import requests
import plotly.graph_objects as go

backend_url = "https://cogniscent-backend-ygrv.onrender.com"

st.set_page_config(page_title="NeuroSync Profile", layout="centered")
st.title("🧠 NeuroSync Cognitive Twin Dashboard")

# === Tabs ===
tab1, tab2 = st.tabs(["🧬 NeuroProfile Generator", "📓 NeuroJournal Reflection"])

with tab1:
    st.markdown("Answer the 7 questions to generate your cognitive twin:")

    with st.form("profile_form"):
        name = st.text_input("Please Enter Your Name (Optional)")
        email = st.text_input("Email Address")
        job_info = st.text_input("Current Job Title and Company")
        goals = st.text_area("Brief Description of Your Career Goals")
        stressors = st.text_area("What Limits Your Productivity at Work?")
        favorite_scent = st.text_input("Favorite Perfume, Cologne, or Candle")
        childhood_scent = st.text_area("Scent Tied to a Positive Childhood Memory")
        submitted = st.form_submit_button("🔮 Generate Profile")

    if submitted:
        job_title = None
        company = None
        if "," in job_info:
            parts = job_info.split(",", 1)
            job_title = parts[0].strip()
            company = parts[1].strip()
        else:
            job_title = job_info.strip()

        data = {
            "name": name,
            "email": email,
            "job_title": job_title,
            "company": company,
            "career_goals": goals,
            "productivity_limiters": stressors,
            "scent_note": favorite_scent,
            "childhood_scent": childhood_scent
        }

        with st.spinner("Analyzing your brain chemistry..."):
            try:
                res = requests.post(f"{backend_url}/generate", json=data)
                if res.status_code == 200:
                    profile = res.json()
                    st.success("Cognitive Twin Generated Successfully!")

                    st.subheader("Neurotransmitter Levels")
                    st.json(profile["neurotransmitters"])

                    st.subheader("Brain Region Scores")
                    st.bar_chart(profile["brain_regions"])

                    st.subheader("Subvector Functions")
                    st.json(profile["subvectors"])

                    st.subheader("🎮 Game & 🎵 Music")
                    st.markdown(f"""
                    **🎮 Game:** {profile['xbox_game']} ({profile['game_mode']})  
                    **🕒 Duration:** {profile['duration_minutes']} mins  
                    **🔄 Switch After:** {profile['switch_time']}  
                    **🎧 Playlist:** {profile['spotify_playlist']}
                    """)

                    # Store for use in reflection
                    st.session_state["profile"] = profile
                    st.session_state["name"] = name

                else:
                    st.error("API error.")
                    st.json(res.json())

            except Exception as e:
                st.error(f"Request failed: {e}")

with tab2:
    st.subheader("📝 NeuroJournal Daily Reflection")
    st.markdown("Use your brain chemistry to generate a personal check-in journal entry.")

    if "profile" not in st.session_state:
        st.warning("⚠️ Please generate your Cognitive Twin in Tab 1 first.")
    else:
        with st.form("reflection_form"):
            mood = st.text_input("How are you feeling today?")
            events = st.text_area("Briefly describe recent events or triggers:")
            goals = st.text_area("What are your short-term or long-term goals?")
            reflect_submit = st.form_submit_button("🧠 Generate Journal Entry")

        if reflect_submit:
            reflection_payload = {
                "name": st.session_state["name"],
                "current_emotion": mood,
                "recent_events": events,
                "goals": goals,
                "neurotransmitters": st.session_state["profile"]["neurotransmitters"],
                "xbox_game": st.session_state["profile"]["xbox_game"],
                "game_mode": st.session_state["profile"]["game_mode"],
                "duration_minutes": st.session_state["profile"]["duration_minutes"],
                "switch_time": st.session_state["profile"]["switch_time"]
            }

            with st.spinner("Crafting your personalized journal..."):
                try:
                    res = requests.post(f"{backend_url}/reflect", json=reflection_payload)
                    if res.status_code == 200:
                        entry = res.json().get("journal_entry", "")
                        st.success("Journal Entry Generated!")
                        st.markdown("#### 🧘 Here's your reflection:")
                        st.markdown(f"> {entry}")
                    else:
                        st.error("Journal generation failed.")
                        st.json(res.json())

                except Exception as e:
                    st.error(f"Reflection failed: {e}")

