import streamlit as st
import requests
import json
import plotly.graph_objects as go

def main():
    st.title("🧬 Visualize Your NeuroProfile")
    st.markdown("Fill out the following to generate your cognitive twin:")

    # Form Inputs
    with st.form("twin_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        gender = st.selectbox("Gender", ["male", "female", "other"])
        scent_note = st.text_input("Favorite Fragrance (e.g., Dior Sauvage)")
        childhood_scent = st.text_area("Describe a vivid childhood scent memory")
        stress_keywords = st.multiselect("Pick 2-3 stress-related keywords", ["deadline", "burnout", "exam", "overwhelmed", "lonely"])
        email = st.text_input("Email (optional)", "")
        job_title = st.text_input("Job Title (optional)", "")
        company = st.text_input("Company (optional)", "")
        career_goals = st.text_area("Career Goals (optional)", "")
        productivity_limiters = st.text_area("Productivity Limiters (optional)", "")
        routine_description = st.text_area("Describe your daily routine")
        region = st.text_input("Where are you from?")

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
