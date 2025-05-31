# Twin_Explorer.py
import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "https://cogniscent-backend-ygrv.onrender.com"

def main():
    st.title("📚 Cognitive Twin Explorer")

    with st.expander("ℹ️ How This Works", expanded=False):
        st.markdown("""
        This dashboard lets developers or researchers explore all generated Cognitive Twins.  
        Filter by demographics to find relevant vectors or download logs for analysis.
        """)

    # === Filter controls ===
    st.sidebar.subheader("🔍 Filter by")
    gender = st.sidebar.selectbox("Gender", ["", "male", "female", "neutral"])
    life_stage = st.sidebar.selectbox("Life Stage", ["", "young_adult", "adult", "senior"])
    age_range = st.sidebar.selectbox("Age Range", ["", "18-25", "25-40", "60+"])
    ethnicity = st.sidebar.selectbox("Ethnicity", ["", "South Asian", "Latinx", "East Asian", "Western", "Other", "Uncategorized"])
    limit = st.sidebar.slider("Limit Results", 1, 100, 25)

    # === Build query params ===
    params = {}
    if gender: params["gender"] = gender
    if life_stage: params["life_stage"] = life_stage
    if age_range: params["age_range"] = age_range
    if ethnicity: params["ethnicity"] = ethnicity
    if limit: params["limit"] = limit

    # === Load from API ===
    try:
        res = requests.get(f"{BACKEND_URL}/twins", params=params)
        res.raise_for_status()
        twins = res.json()

        if not twins:
            st.warning("No cognitive twins match the selected filters.")
            return

        df = pd.DataFrame(twins)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values(by="timestamp", ascending=False)

        st.success(f"Loaded {len(df)} matching twins")

        st.dataframe(df[["name", "gender", "life_stage", "age_range", "ethnicity", "timestamp", "vector_id"]])

        csv = df.to_csv(index=False)
        st.download_button("📥 Download CSV", data=csv, file_name="filtered_twins.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Failed to load twins: {e}")
