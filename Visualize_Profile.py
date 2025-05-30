import streamlit as st
import requests
import plotly.graph_objects as go

def main():
    st.title("🧬 Visualize Your NeuroProfile")
    st.markdown("Answer the following 7 questions to generate your Cognitive Twin:")

    # Form Inputs
    with st.form("profile_form"):
        name = st.text_input("Please Enter Your Name (Optional)")
        email = st.text_input("Email Address")
        job_info = st.text_input("Current Job Title and Company")
        goals = st.text_area("Brief Description of Your Career Goals (e.g., promotion, startup founder, etc.)")
        stressors = st.text_area("Things That Limit Your Productivity and Performance in the Workplace")
        favorite_scent = st.text_input("Favorite Perfume, Cologne, or Candle")
        childhood_scent = st.text_area("Describe a Positive Association You Have with a Scent from Childhood")
        
        submitted = st.form_submit_button("Generate NeuroProfile")

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

        st.subheader("🔍 Debug: Payload being sent")
        st.json(data)

        with st.spinner("Analyzing your brain chemistry..."):
            try:
                res = requests.post("https://cogniscent-backend-ygrv.onrender.com/generate", json=data)
                if res.status_code == 200:
                    profile = res.json()
                    st.success("🧠 Cognitive Twin Generated Successfully!")

                    st.subheader("Neurotransmitter Levels")
                    st.json(profile["neurotransmitters"])

                    st.subheader("Brain Region Scores")
                    st.bar_chart(profile["brain_regions"])

                    st.subheader("Region Subvectors")
                    st.json(profile["subvectors"])
                    
                    st.subheader("🎮 Xbox Game & 🎵 Spotify Recommendation")
                    st.info(f"""
                    🎮 **{profile.get("xbox_game", "N/A")}** ({profile.get("game_mode", "N/A")})  
                    ⏱️ Play for: **{profile.get("duration_minutes", "N/A")} mins**, then switch: **{profile.get("switch_time", "N/A")}**  
                    🎧 Playlist: **{profile.get("spotify_playlist", "N/A")}**
                    """)
                    
                    st.subheader("🔬 NeuroReflection Insights")
                    mood_insights = []
                    nt = profile["neurotransmitters"]
                    if nt["dopamine"] > 0.6:
                        mood_insights.append("You may feel energetic or reward-driven today.")
                    if nt["cortisol"] > 0.6:
                        mood_insights.append("Heightened cortisol suggests stress — consider grounding activities.")
                    if nt["GABA"] < 0.4:
                        mood_insights.append("Low GABA may reflect restlessness or low inhibition.")

                    st.markdown("**🧠 Mood Interpretation:**")
                    st.markdown("• " + "\n• ".join(mood_insights) if mood_insights else "Your neurotransmitters are balanced today.")

                    # Scent recommendations
                    st.markdown("**🌸 Scent Recommendations:**")
                    if nt["cortisol"] > 0.6:
                        st.markdown("- Try **lavender** or **linalool** for calming effects (boosts GABA).")
                    elif nt["dopamine"] < 0.4:
                        st.markdown("- Try **cinnamon** or **mint** to enhance motivation (dopamine boosters).")
                    else:
                        st.markdown("- Maintain balance with **vanilla** or **rose** to support oxytocin and emotional grounding.")

                    # Playlist logic
                    st.markdown("**🎵 Why this Playlist?**")
                    playlist = profile.get("spotify_playlist", "")
                    if "Focus" in playlist:
                        st.markdown("- Designed to sustain attention and working memory via dopamine and serotonin pathways.")
                    elif "Chill" in playlist:
                        st.markdown("- Helps reduce stress and soothe heightened amygdala activity.")
                    else:
                        st.markdown("- Selected to match your emotional tone and neurotransmitter balance.")

                    # Game strategy explanation
                    st.markdown("**🎮 Game Strategy:**")
                    game = profile.get("xbox_game", "the game")
                    mode = profile.get("game_mode", "your current mode")
                    duration = profile.get("duration_minutes", "30")
                    switch = profile.get("switch_time", "15 mins")

                    st.markdown(f"- **{game}** was selected to engage your **{mode}**-oriented mindset.")
                    st.markdown(f"- Play for **{duration} minutes**, then switch every **{switch}** to avoid overstimulation.")
                    st.markdown("- This pattern supports healthy **prefrontal cortex** engagement and avoids amygdala fatigue.")

                else:
                    st.error(f"Something went wrong. Status code: {res.status_code}")
                    st.text("Raw response:")
                    st.json(res.json())
            except Exception as e:
                st.error(f"Request failed: {e}")

if __name__ == "__main__":
    main()
