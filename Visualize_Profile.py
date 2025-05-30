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

                else:
                    st.error(f"Something went wrong. Status code: {res.status_code}")
                    st.text("Raw response:")
                    st.json(res.json())
            except Exception as e:
                st.error(f"Request failed: {e}")

if __name__ == "__main__":
    main()
