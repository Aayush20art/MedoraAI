# Medora AI 💊
### Smart HealthCare Prediction System

🚀 **Live Demo:**  
https://medoraai-f9jvenhgazbhd9zaugcmbb.streamlit.app/

---

# 📌 Overview

Medora AI is an advanced AI-powered healthcare analytics platform built using Streamlit, Machine Learning, SHAP Explainable AI, NLP, and RAG (Retrieval-Augmented Generation).

The platform provides intelligent clinical prediction systems for:

- 🫀 Heart Disease Prediction
- 🩸 Diabetes Prediction
- 🏨 ICU Readmission Risk Analysis
- 📄 Medical Report NLP Analysis
- ⚕️ AI PDF Medical Assistant

Medora AI combines predictive analytics with explainable AI to help users better understand healthcare risks and clinical reports.

---

# ✨ Features

## 🫀 Heart Disease Prediction
- Predicts cardiac disease risk using ML models
- Displays probability score and confidence
- SHAP Explainable AI visualization
- Interactive clinical dashboard

---

## 🩸 Diabetes Prediction
- Diabetes risk analysis using patient parameters
- Estimated HbA1c prediction
- SHAP-based feature importance analysis

---

## 🏨 ICU Readmission Prediction
- Calculates ICU readmission risk
- Uses LACE-style scoring mechanism
- Risk factor contribution breakdown

---

## 📄 Medical NLP Analyzer
- Extracts:
  - Diseases
  - Symptoms
  - Medications
  - Anatomy terms
  - Vital signs

- Annotates medical reports automatically
- Generates clinical risk score

---

## ⚕️ AI PDF Medical Assistant
- Upload medical PDFs
- Ask questions in natural language
- RAG-powered contextual answers
- Explains medical terms in simple language

---

## 📊 Patient History Dashboard
- Stores prediction history
- Displays scan statistics
- Risk distribution visualization

---

# 🛠️ Tech Stack

## Frontend
- Streamlit
- Custom CSS UI
- Interactive Charts

---

## Backend
- Python
- Machine Learning Models
- SHAP Explainable AI
- RAG Pipeline
- NLP Processing

---

## Libraries Used

```bash
streamlit
pandas
numpy
matplotlib
joblib
shap
langchain
langchain-community
langchain-huggingface
groq
PyPDF2
sentence-transformers
```

---

# 🤖 AI & ML Technologies

- Machine Learning Classification Models
- SHAP Explainable AI
- NLP Entity Recognition
- RAG (Retrieval-Augmented Generation)
- Embedding-based PDF Search
- Groq LLM Integration

---

# 📂 Project Structure

```bash
Medora-AI/
│
├── app.py
├── medoraAI_css.py
├── requirements.txt
├── .streamlit/
│   └── secrets.toml
│
├── models/
│   ├── diabetes_model.pkl
│   ├── diabetes_scaler.pkl
│   ├── diabetes_features.pkl
│   ├── heart_model.pkl
│   ├── heart_scaler.pkl
│   └── heart_features.pkl
│
└── assets/
```

---

# 🔑 Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/medora-ai.git

cd medora-ai
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Add Groq API Key

Create:

```bash
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

---

## 4️⃣ Run Application

```bash
streamlit run app.py
```

---

# 📈 Core Functionalities

| Module | Description |
|---|---|
| Heart Disease | Cardiac risk prediction |
| Diabetes | Diabetes probability analysis |
| ICU Readmission | ICU relapse prediction |
| NLP Analyzer | Clinical entity extraction |
| PDF Assistant | AI medical chatbot |
| SHAP XAI | Explainable predictions |

---

# 🎯 Key Highlights

- Modern Healthcare UI
- Explainable AI (XAI)
- Real-time Predictions
- AI-powered PDF Chat
- Clinical NLP Engine
- Interactive Risk Visualizations
- Groq LLM Integration
- RAG-based Contextual Understanding

---

# ⚠️ Disclaimer

This project is developed for educational and research purposes only and should not be considered professional medical advice.

---

# 🌟 Future Improvements

- Multi-disease prediction
- Real-time EHR integration
- Voice-based medical assistant
- Medical image analysis
- Cloud deployment pipeline
- Advanced clinical NLP models

---

# 📸 Live Application

🔗 https://medoraai-f9jvenhgazbhd9zaugcmbb.streamlit.app/

---

# ⭐ Support

If you liked this project, consider giving it a ⭐ on GitHub.
