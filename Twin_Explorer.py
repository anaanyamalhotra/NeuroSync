# Twin_Explorer.py
import streamlit as st
import requests
import pandas as pd
import ast

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
    limit = st.sidebar.slider("Limit Results", 1, 100, 25)

    # === Build query params ===
    params = {}
    if gender: params["gender"] = gender
    if life_stage: params["life_stage"] = life_stage
    if age_range: params["age_range"] = age_range
    if limit: params["limit"] = limit

    # === Load from API ===
    try:
        res = requests.get(f"{BACKEND_URL}/twins", params=params)
        res.raise_for_status()
        twins = res.json().get("twins", [])

        if not twins:
            st.warning("No cognitive twins match the selected filters.")
            return

        df = pd.DataFrame(twins)
        if "timestamp" not in df.columns:
            df["timestamp"] = "unknown"
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values(by="timestamp", ascending=False)

        def get_top_nts(neuro_dict, top_n=2):
            if isinstance(neuro_dict, dict):
                sorted_nts = sorted(neuro_dict.items(), key=lambda x: x[1], reverse=True)
                return ", ".join([f"{k} ({v:.2f})" for k, v in sorted_nts[:top_n]])
            return ""
        if "neurotransmitters" in df.columns:
            df["top_neurotransmitters"] = df["neurotransmitters"].apply(get_top_nts)
        elif "twin_vector" in df.columns:
            df["top_neurotransmitters"] = df["twin_vector"].apply(
                lambda twin: get_top_nts(twin.get("neurotransmitters", {})) if isinstance(twin, dict) else ""
            )
        else:
            df["top_neurotransmitters"] = ""
            
                

        st.success(f"Loaded {len(df)} matching twins")

        st.dataframe(df[["name", "gender", "life_stage", "age_range", "timestamp", "vector_id"]])

        csv = df.to_csv(index=False)
        st.download_button("📥 Download CSV", data=csv, file_name="filtered_twins.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Failed to load twins: {e}")
