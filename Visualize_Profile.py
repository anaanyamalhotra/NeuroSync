import streamlit as st
import requests
import plotly.graph_objects as go
from difflib import get_close_matches

st.cache_data.clear()
st.cache_resource.clear()

backend_url = "https://cogniscent-backend-ygrv.onrender.com"

st.set_page_config(page_title="NeuroSync Profile", layout="centered")
st.title("🧠 NeuroSync Cognitive Twin Dashboard")

# === Tabs ===
tab1, tab2 = st.tabs(["🧬 NeuroProfile Generator", "📓 NeuroJournal Reflection"])

with tab1:

    with st.expander("🧭 How This Works", expanded=False):
        st.markdown("""
        NeuroSync creates a personalized 'Cognitive Twin' using scent preferences, career data, and stress triggers.  
        It maps neurotransmitter activity, brain region profiles, and generates tailored game & music recommendations.
        Just answer 7 simple questions — your mind’s mirror is one click away.
        """)
        
    st.markdown("Answer the 7 questions to generate your cognitive twin:")

    with st.form("profile_form"):
        name = st.text_input("Please Enter Your Name", help="Used only for personalization. Not stored.")
        email = st.text_input("Email Address", help="Required for journaling. Not shared.")
        job_info = st.text_input("Current Job Title and Company", help="E.g., 'Student, University of X' or 'Engineer, Microsoft'")
        goals = st.text_area("Career Goals", help="What do you aim to achieve professionally?")
        stressors = st.text_area("Workplace Limiters", help="What affects your productivity or focus?")
        favorite_scent = st.text_input("Favorite Perfume/Candle", help="Used to stimulate neurotransmitter modeling.")
        childhood_scent = st.text_area("Positive Scent Memory", help="Recall a scent from childhood with emotional value.")
        submitted = st.form_submit_button("🧠 Generate Cognitive Twin")
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
                st.write("DEBUG — HTTP status code:", res.status_code)
                try:
                    profile = res.json()
                    st.write("DEBUG — parsed JSON from /generate:", profile)
                except Exception:
                    st.write("DEBUG — response was not valid JSON. Raw text:")
                    st.text(res.text)
                    return
                
                if res.status_code == 200:
                    profile = res.json()
                    if profile.get("status") == "error":
                        st.error(f"❌ Server Error: {profile.get('message', 'Unknown issue.')}")
                        return
                    if "neurotransmitters" not in profile:
                        st.error("❌ Backend did not return neurotransmitter data. Please check inputs or try again.")
                        st.write("DEBUG profile received from backend:", profile)
                        return
                    st.success("Cognitive Twin Generated Successfully!")

                    st.subheader("Neurotransmitter Levels")
                    st.json(profile["neurotransmitters"])

                    st.subheader("Brain Region Scores")
                    st.bar_chart(profile["brain_regions"])

                    weights = {
                    "dopamine": 0.25,
                    "serotonin": 0.25,
                    "oxytocin": 0.2,
                    "GABA": 0.2,
                    "cortisol": -0.15

                    }
                    nt = profile["neurotransmitters"]
                    mood_score = sum(nt.get(k, 0) * w for k, w in weights.items())
                    mood_score = max(0, min(1, mood_score)) * 100
                    mood_score = round(mood_score, 1)
                    st.subheader("🧠 Mood Score")
                    st.metric(label="Mood Balance Score", value=f"{mood_score}/100")
                    thermometer = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=mood_score,
                        title={"text": "Mood Thermometer"},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "deepskyblue"},
                            "steps": [
                                {"range": [0, 40], "color": "lightcoral"},
                                {"range": [40, 70], "color": "khaki"},
                                {"range": [70, 100], "color": "lightgreen"},
                            ],
                        }
                    ))
                    st.plotly_chart(thermometer)

                    

                    st.subheader("Subvector Functions")
                    st.json(profile["subvectors"])

                    st.subheader("🎮 Game & 🎵 Music")
                    st.markdown(f"""
                    **🎮 Game:** {profile['xbox_game']} ({profile['game_mode']})  
                    **🕒 Duration:** {profile['duration_minutes']} mins  
                    **🔄 Switch After:** {profile['switch_time']}  
                    """)
                    st.subheader("🧠 Why This Game?")
                    
                    def find_game_entry(name):
                        try:
                            game_name = name.lower().strip()
                            for g in game_profiles:
                                if g["name"].lower() == game_name:
                                    return g
                            matches = get_close_matches(game_name, [g["name"].lower() for g in game_profiles], n=1)
                            if matches:
                                return next((g for g in game_profiles if g["name"].lower() == matches[0]), None)
                            return None
                        except:
                            return None

                    matched_game = find_game_entry(profile["xbox_game"])

                    if matched_game:
                        st.markdown(f"**Psychological Effects:** {', '.join(matched_game.get('psychological_effects', []))}")
                        st.markdown(f"**Targeted Neurotransmitters:** {', '.join(matched_game.get('tags', []))}")
                        st.markdown(f"**Brain Regions Stimulated:** {', '.join(matched_game.get('brain_region_activation', []))}")
                        st.markdown(f"**Challenge Level:** {matched_game.get('challenge_level', 'moderate').capitalize()}")

                        scent_used = profile.get("scent_note", "").lower().strip()
                        affinity_score = matched_game.get("scent_affinity", {}).get(scent_used)
                        if affinity_score:
                            st.markdown(f"**🌸 Matching Scent Affinity:** {scent_used.title()} (score: {affinity_score})")
                    if "match_reason" in profile:
                        st.info(f"🧠 Matching Rationale: {profile['match_reason']}")
                            
        
                    st.subheader("🎧 Personalized Spotify Playlist")
                    st.info(f"**Recommended Based on Brain Chemistry:** _{profile['spotify_playlist']}_")
                    st.subheader("🌿 Olfactory Suggestion")
                    st.markdown(f"Try using **{profile['scent_reinforcement']}** today to support your mental balance.")

                    region_explanations = {
                        "amygdala": "The amygdala helps regulate emotions and threat response. A calming scent like lavender may reduce hyperactivity here by increasing GABA and decreasing cortisol.",
                        "prefrontal_cortex": "This region supports focus and decision-making. Energizing scents like mint or cinnamon can boost dopamine levels to aid executive function.",
                        "hippocampus": "The hippocampus handles memory and learning. Scents like bergamot or citrus may enhance serotonin and support memory encoding.",
                        "hypothalamus": "The hypothalamus regulates stress and hormone balance. GABA-enhancing scents like linalool may help restore calm and emotional stability."
                    }

                    lowest_region = profile.get("lowest_region", "")
                    if lowest_region and lowest_region in region_explanations:
                        st.subheader("🧪 NeuroScientific Insight")
                        st.markdown(region_explanations[lowest_region])

                    # Store for use in reflection
                    st.session_state["profile"] = profile
                    st.session_state["twin_data"] = profile 
                    st.session_state["name"] = name

                else:
                    st.error("API error.")
                    try:
                        st.json(res.json())
                    except Exception:
                        st.text(res.text)

            except Exception as e:
                st.error(f"Request failed: {e}")

with tab2:
    with st.expander("📓 How Reflections Work", expanded=False):
        st.markdown("""
        Your cognitive twin powers this journaling system. 
        Based on your brain chemistry, we help you process emotions and uncover patterns.
        Reflect regularly to see mood trends and track cognitive wellness over time.
        """)

    if "emotion_timeline" not in st.session_state:
        st.session_state["emotion_timeline"] = []
    if "feedback_log" not in st.session_state:
        st.session_state["feedback_log"] = []
    st.subheader("📝 NeuroJournal Daily Reflection")
    st.markdown("Use your brain chemistry to generate a personal check-in journal entry.")

    if "profile" not in st.session_state:
        st.warning("⚠️ Please generate your Cognitive Twin in Tab 1 first.")
    else:
        with st.form("reflection_form"):
            mood = st.text_input("Current Mood", help="How do you feel right now?")
            events = st.text_area("Recent Events", help="Describe events or stressors influencing your day.")
            goals = st.text_area("Your Goals", help="Short or long-term goals you want to focus on.")
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
                        mood_keywords = reflection_payload["current_emotion"].lower().split()
                        positive_words = ["happy", "hopeful", "excited", "motivated"]
                        negative_words = ["anxious", "sad", "tired", "overwhelmed"]
                        score = sum(1 for w in mood_keywords if w in positive_words) - sum(1 for w in mood_keywords if w in negative_words)
                        normalized_score = round((score + 3) / 6, 2) 
                        st.session_state["emotion_timeline"].append(normalized_score)
                        st.subheader("📈 Mood Timeline")
                        st.line_chart(st.session_state["emotion_timeline"])
                        st.subheader("🗣️ How helpful was this reflection?")
                        feedback = st.slider("Rate this reflection (0 = Not helpful, 5 = Very helpful)", 0, 5, 3)
                        st.session_state["feedback_log"].append(feedback)
                        st.markdown(f"✅ Logged mood score: **{normalized_score}**, Feedback: **{feedback}**")
                        import pandas as pd
                        from io import BytesIO
                        if st.session_state["emotion_timeline"] and st.session_state["feedback_log"]:
                            df_log = pd.DataFrame({
                                "Timestamp": pd.date_range(end=pd.Timestamp.now(), periods=len(st.session_state["emotion_timeline"]), freq="T"),
                                "Mood Score": st.session_state["emotion_timeline"],
                                "Feedback": st.session_state["feedback_log"]
                            })
                            st.subheader("🧾 Download Mood & Feedback History")
                            buffer = BytesIO()
                            df_log.to_csv(buffer, index=False)
                            buffer.seek(0)
                            st.download_button(
                                label="📥 Download Log as CSV",
                                data=buffer,
                                file_name="neuro_journal_log.csv",
                                mime="text/csv"
                            )
                            import numpy as np
                            if st.session_state["emotion_timeline"]:
                                scores = np.array(st.session_state["emotion_timeline"])
                                volatility = round(np.std(scores), 2)
                                avg_score = round(np.mean(scores), 2)
                                recent_trend = "📈 Improving" if scores[-1] > scores[0] else "📉 Declining"
                                st.subheader("📊 Mood Summary Analytics")
                                st.markdown(f"""
                                - **Average Mood Score:** {avg_score}  
                                - **Mood Volatility (Std Dev):** {volatility}  
                                - **Trend Over Time:** {recent_trend}  
                                """)

                    else:
                        st.error("Journal generation failed.")
                        st.json(res.json())

                except Exception as e:
                    st.error(f"Reflection failed: {e}")

