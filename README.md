# NeuroSync – Cognitive Twin App (Frontend)

This is the Streamlit frontend of NeuroSync, a neuroscience-inspired Cognitive Twin app. Users enter 7 inputs (job, goals, stressors, scent preferences, etc.), and the UI displays their neurotransmitter profile, brain region activity, Xbox game recommendation, and Spotify playlist suggestion. Includes journaling and a developer twin explorer.

## Features
- Streamlit-based interface with tabs for:
  - 🧬 NeuroProfile Generator: Input form, profile generation, visualization
  - 📓 NeuroJournal Reflection: GPT-powered journaling and emotional insight
  - 📚 Cognitive Twin Explorer: Admin tool to filter and download cognitive twins

## Requirements
- Python 3.8+
- Streamlit, requests, pandas, plotly

## Setup
```bash
pip install streamlit pandas numpy requests plotly
streamlit run app.py
```

## Folder Overview
- `app.py`: Multipage launcher
- `Visualize_Profile.py`: User input form + results
- `Reflection.py`: GPT journaling logic
- `Twin_Explorer.py`: Twin explorer with filters
- Backend assumed to be deployed separately with working endpoints for `/generate`, `/reflect`, and `/twins`

## Deployment
- Deploy on [Streamlit Cloud](https://share.streamlit.io/)
- Update `BACKEND_URL` inside the `.py` files to match your FastAPI backend (e.g., https://cogniscent-backend.onrender.com)

## Live Demo
- 🌐 Frontend App: [https://neurosync-ananya.streamlit.app/](https://neurosync-ananya.streamlit.app/)
- 🧠 Backend API: [https://cogniscent-backend-ygrv.onrender.com](https://cogniscent-backend-ygrv.onrender.com)

## How It Works
1. User fills out a 7-question form
2. Data is sent to the FastAPI backend
3. Backend responds with:
   - Top neurotransmitters
   - Brain region scores
   - Game + music recommendations
   - Scent reinforcement
4. Streamlit displays results in tabs with expandable explanations

## Output Example
- Dopamine: 0.71, Serotonin: 0.77, Oxytocin: 0.72
- Game: *Journey to the Savage Planet*
- Playlist: Focus Boost
- Scent Reinforcement: Linalool or Vanilla

## Author
Ananya Malhotra
