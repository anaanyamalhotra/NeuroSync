import streamlit as st
import requests
import json
import plotly.graph_objects as go

def main():
    st.title("🧬 Visualize Your NeuroProfile")
    st.markdown("Fill out the following to generate your cognitive twin:")

    # Form Inputs
    with st.form("profile_form"):
        name = st.text_input("Please Enter Your Name (Optional)")
        email = st.text_input("Email Address")
        job = st.text_input("Current Job Title and Company")
        goals = st.text_area("Brief Description of Your Career Goals")
        stressors = st.text_area("Things That Limit Your Productivity in the Workplace")
        favorite_scent = st.text_input("Favorite Perfume, Cologne, or Candle")
        childhood_scent = st.text_area("Positive Association You Have with a Childhood Scent")
    
        submitted = st.form_submit_button("Generate NeuroProfile")

    if submitted:
        data = {
            "name": name,
            "age": age,
            "gender": gender,
            "scent_note": scent_note,
            "childhood_scent": childhood_scent,
            "stress_keywords": stress_keywords,
            "email": email,
            "job_title": job_title,
            "company": company,
            "career_goals": career_goals,
            "productivity_limiters": productivity_limiters,
            "routine_description": routine_description,
            "region": region
        }

        with st.spinner("Analyzing your brain chemistry..."):
            try:
                res = requests.post("https://cogniscent-backend-ygrv.onrender.com/generate", json=data)
                if res.status_code == 200:
                    profile = res.json()
                    st.success("Cognitive Twin Generated Successfully!")

                    st.subheader("🧠 Neurotransmitter Levels")
                    st.json(profile["neurotransmitters"])

                    st.subheader("🧠 Brain Region Scores")
                    st.bar_chart(profile["brain_regions"])

                    st.subheader("🧠 Region Subvectors")
                    st.json(profile["subvectors"])

                else:
                    st.error("Error generating profile. Please try again.")
            except Exception as e:
                st.error(f"Request failed: {e}")

if __name__ == "__main__":
    main()
