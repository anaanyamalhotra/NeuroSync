
# 🎛️ Cogniscent Frontend (Streamlit)

This is the Streamlit-based frontend for the Cognitive Twin Intelligence Platform. It allows users to input personal and emotional data, view their neuroprofile, and receive personalized recommendations and reflections.

## 🧩 Features

- Collects user data (name, age, gender, scent, stressors, goals, routine)
- Displays neurotransmitter vector and brain region breakdown
- Shows personalized game and music recommendations
- Generates a GPT-powered reflection: "Why do I feel this way?"
- Export profile as a downloadable PDF

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Make sure your backend is running locally or on Render.

## 📦 Requirements

- streamlit
- pandas
- plotly
- requests
- fpdf (for PDF export)
