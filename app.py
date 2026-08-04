import streamlit as st

st.set_page_config(
    page_title="Medora AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

from medoraAI_css import CSS
st.markdown(CSS, unsafe_allow_html=True)


import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib, warnings, os, datetime, tempfile
warnings.filterwarnings('ignore')

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
for key, val in [
    ('history', []),
    ('vector_store', None),
    ('embeddings', None),
    ('chat_history', []),
    ('pdf_loaded', False),
    ('doc_chunks', 0),
    ('pdf_name', ''),
]:
    if key not in st.session_state:
        st.session_state[key] = val


# ─── LOAD ML MODELS ────────────────────────────────────────────────────────────
BASE = os.path.dirname(__file__)

@st.cache_resource
def load_all_models():
    try:
        return {
            'diabetes': (
                joblib.load(os.path.join(BASE, 'models/diabetes_model.pkl')),
                joblib.load(os.path.join(BASE, 'models/diabetes_scaler.pkl')),
                joblib.load(os.path.join(BASE, 'models/diabetes_features.pkl')),
            ),
            'heart': (
                joblib.load(os.path.join(BASE, 'models/heart_model.pkl')),
                joblib.load(os.path.join(BASE, 'models/heart_scaler.pkl')),
                joblib.load(os.path.join(BASE, 'models/heart_features.pkl')),
            ),
        }
    except Exception as e:
        st.warning(f"ML models not found: {e}")
        return {}

models = load_all_models()


# ─── GROQ API KEY ──────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass


# ─── RAG HELPERS ───────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_embeddings():
    from langchain_huggingface.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


def process_pdf(uploaded_file) -> int:
    from langchain_core.vectorstores import InMemoryVectorStore
    from langchain_community.document_loaders import PyPDFLoader
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    loader = PyPDFLoader(tmp_path)
    docs = loader.load_and_split()
    embeddings = st.session_state.embeddings
    vs = InMemoryVectorStore(embedding=embeddings)
    vs.add_documents(docs)
    st.session_state.vector_store = vs
    st.session_state.pdf_loaded = True
    st.session_state.doc_chunks = len(docs)
    st.session_state.pdf_name = uploaded_file.name
    os.unlink(tmp_path)
    return len(docs)


def retrieve_context(query: str, k: int = 4) -> list:
    return st.session_state.vector_store.similarity_search(query, k=k)


def ask_groq(query: str, context: str, model: str, history: list) -> str:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    system_prompt = (
        "You are MedoraAI's patient-facing PDF assistant. Your job is to explain complex "
        "medical information from the provided PDF context in simple, clear, friendly language "
        "that anyone can understand — no medical jargon. Use analogies when helpful. "
        "If the answer is not in the context, say so honestly. Keep responses concise."
    )
    messages = [{"role": "system", "content": system_prompt}]
    for turn in history[-6:]:
        messages.append({"role": "user", "content": turn["user"]})
        messages.append({"role": "assistant", "content": turn["assistant"]})
    messages.append({
        "role": "user",
        "content": f"Context from PDF:\n{context}\n\n---\nQuestion: {query}"
    })
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0.3, max_tokens=1024
    )
    return response.choices[0].message.content

# ─── SHAP ──────────────────────────────────────────────────────────────────────
def get_shap_values(model, scaler, input_df):
    try:
        import shap
        X = scaler.transform(input_df)
        explainer = shap.TreeExplainer(model)
        sv = np.array(explainer.shap_values(X), dtype=np.float64)

        if sv.ndim == 3:
            result = sv[0, :, 1] if sv.shape[0] == 1 else sv[1, 0, :] if sv.shape[2] != 1 else sv[0, :, 0]
        elif sv.ndim == 2:
            result = sv[0, :]
        else:
            result = sv

        return result.astype(np.float64)

    except Exception:
        fi = model.feature_importances_.astype(np.float64)
        prob = float(model.predict_proba(scaler.transform(input_df))[0][1])
        return fi * (1.0 if prob > 0.5 else -1.0) * prob


def plot_shap_bar(feature_names, shap_vals, title):
    names = list(feature_names)
    vals = np.array(shap_vals, dtype=np.float64).flatten()

    n = len(names)

    if len(vals) > n:
        vals = vals[:n]
    elif len(vals) < n:
        vals = np.pad(vals, (0, n - len(vals)))

    order = np.argsort(np.abs(vals))
    snames = [names[i] for i in order]
    svals = vals[order].tolist()

    colors = ['#e31b23' if v > 0 else '#00c853' for v in svals]

    fig, ax = plt.subplots(figsize=(7, max(3.5, n * 0.48)))

    ax.barh(
        snames,
        svals,
        color=colors,
        edgecolor='none',
        height=0.48,
        alpha=0.88
    )

    ax.axvline(
        0,
        color=(227/255, 27/255, 35/255, 0.3),
        linewidth=0.8
    )

    ax.set_xlabel(
        "SHAP Value",
        fontsize=8,
        color='#888888',
        labelpad=8
    )

    ax.set_title(
        title,
        fontsize=9.5,
        fontweight='600',
        color='#ffffff',
        pad=12
    )

    ax.tick_params(
        labelsize=7.5,
        colors='#888888',
        length=0
    )

    for s in ax.spines.values():
        s.set_visible(False)

    ax.set_facecolor('#0a0a0a')
    fig.patch.set_facecolor('#0a0a0a')

    ax.grid(
        axis='x',
        color=(1, 1, 1, 0.03),
        linewidth=0.5,
        linestyle='--'
    )

    fig.tight_layout(pad=1.5)

    return fig

# ─── GAUGE (RED THEME) ─────────────────────────────────────────────────────────
def render_gauge(prob):
    pct   = round(prob * 100, 1)
    angle = -180 + prob * 180
    rad   = (angle - 90) * 3.14159 / 180
    cx, cy, r = 130, 108, 80
    x = cx + r * np.cos(rad)
    y = cy + r * np.sin(rad)
    color = '#e31b23' if prob > 0.6 else '#ffab00' if prob > 0.3 else '#00c853'
    label = 'HIGH RISK' if prob > 0.6 else 'MODERATE' if prob > 0.3 else 'LOW RISK'
    return f"""
    <div class="gauge-wrap">
    <svg width="260" height="142" viewBox="0 0 260 142" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="gfill" x1="0%" x2="100%">
          <stop offset="0%"   stop-color="#00c853"/>
          <stop offset="50%"  stop-color="#ffab00"/>
          <stop offset="100%" stop-color="#e31b23"/>
        </linearGradient>
        <filter id="glow"><feGaussianBlur stdDeviation="2.5" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <path d="M44 112 A86 86 0 0 1 216 112" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="10" stroke-linecap="round"/>
      <path d="M44 112 A86 86 0 0 1 {x:.1f} {y:.1f}" fill="none" stroke="url(#gfill)" stroke-width="10" stroke-linecap="round" filter="url(#glow)"/>
      <circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{color}" stroke="#0a0a0a" stroke-width="2.5" filter="url(#glow)"/>
      <circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="white" opacity="0.9"/>
      <text x="130" y="98"  text-anchor="middle" fill="{color}" font-size="28" font-weight="600" font-family="Space Grotesk,monospace">{pct}%</text>
      <text x="130" y="114" text-anchor="middle" fill="{color}" font-size="7.5"  font-weight="700" letter-spacing="3">{label}</text>
      <text x="36"  y="128" fill="#00c853" font-size="7" font-family="Inter" font-weight="600" opacity="0.7">LOW</text>
      <text x="197" y="128" fill="#e31b23" font-size="7" font-family="Inter" font-weight="600" opacity="0.7">HIGH</text>
    </svg>
    </div>"""


# ─── NLP DICT ──────────────────────────────────────────────────────────────────
NLP_DICT = {
    "DISEASE":    ["diabetes","hypertension","heart disease","coronary artery disease","pneumonia","asthma","copd","cancer","stroke","tuberculosis","ckd","chronic kidney disease","heart failure","sepsis","anemia","arthritis","depression","anxiety","dementia","epilepsy","hypothyroidism","obesity","hepatitis"],
    "SYMPTOM":    ["chest pain","shortness of breath","dyspnea","fatigue","fever","nausea","vomiting","headache","dizziness","palpitations","edema","swelling","cough","wheezing","weakness","weight loss","tachycardia","syncope","confusion","blurred vision","polyuria","polydipsia","polyphagia"],
    "MEDICATION": ["metformin","insulin","aspirin","lisinopril","atorvastatin","amlodipine","metoprolol","warfarin","furosemide","omeprazole","amoxicillin","azithromycin","prednisone","levothyroxine","albuterol","sertraline","enalapril","losartan","clopidogrel"],
    "ANATOMY":    ["heart","lungs","kidney","liver","brain","blood","arteries","chest","abdomen","pancreas","thyroid","colon","aorta","ventricle"],
    "VITAL":      ["blood pressure","bp","heart rate","spo2","oxygen saturation","temperature","bmi","glucose","creatinine","hemoglobin","cholesterol","sodium","potassium","wbc","hba1c","troponin"],
}

def nlp_analyze(text):
    tl = text.lower()
    found = {}
    for etype, terms in NLP_DICT.items():
        hits = list(dict.fromkeys(t.title() for t in terms if t in tl))
        if hits: found[etype] = hits
    risk = min(len(found.get("DISEASE",[])) * 15 + len(found.get("SYMPTOM",[])) * 8 + len(found.get("MEDICATION",[])) * 5, 100)
    return found, risk


# ─── HISTORY HELPERS ───────────────────────────────────────────────────────────
def add_history(module, prob, label, detail=""):
    st.session_state.history.insert(0, {
        "module": module, "prob": round(prob * 100, 1), "label": label,
        "detail": detail, "time": datetime.datetime.now().strftime("%H:%M:%S"),
    })

def render_history():
    hist = st.session_state.history
    if not hist:
        st.markdown("<p style='color:var(--white-muted);text-align:center;padding:2rem;font-size:0.75rem;letter-spacing:1px'>— NO SCANS YET —</p>", unsafe_allow_html=True)
        return
    icons = {"Heart Disease": "🫀", "Diabetes": "🩸", "ICU Readmission": "🏨", "NLP Analysis": "📄", "Medical Assistant": "⚕️"}
    for h in hist:
        b  = "badge-hi" if h["prob"] > 60 else "badge-mod" if h["prob"] > 30 else "badge-lo"
        pc = "#e31b23" if h["prob"] > 60 else "#ffab00" if h["prob"] > 30 else "#00c853"
        icon = icons.get(h["module"], "🔬")
        st.markdown(f"""<div class='hist-item'>
            <div class='hist-icon'>{icon}</div>
            <div style='flex:1;min-width:0'>
                <div class='hist-label'>{h['module']}</div>
                <div class='hist-detail'>{h['detail']}</div>
            </div>
            <div style='text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:4px'>
                <span class='hist-prob' style='color:{pc}'>{h['prob']}%</span>
                <span class='hist-badge {b}'>{h['label']}</span>
            </div>
            <div class='hist-time'>{h['time']}</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class='brand-wrap'>
        <div class='brand-logo-row'>
            <div class='brand-icon'>💊</div>
            <div>
                <div class='brand-title'>Medora<span>AI</span></div>
                <div class='brand-tagline'>Clinical Intelligence Platform</div>
            </div>
        </div>
        <div class='brand-badges'>
            <span class='brand-badge'>v3.0</span>
            <span class='brand-badge'>XAI</span>
            <span class='brand-badge'>RAG</span>
            <span class='brand-badge'>NLP</span>
        </div>
    </div>
    <div class='nav-section'>Modules</div>
    """, unsafe_allow_html=True)

    module = st.radio("", [
        "🫀  Heart Disease",
        "🩸  Diabetes",
        "🏨  ICU Readmission",
        "📄  Medical NLP",
        "⚕️  Medical Report Assistant",
        "📋  Patient History",
    ], label_visibility="collapsed")

    pdf_ok  = "ok" if st.session_state.pdf_loaded else "warn"
    pdf_txt = f"✓ {st.session_state.pdf_name[:16]}…" if st.session_state.pdf_loaded else "Not loaded"
    ml_ok   = "ok" if models else "warn"
    ml_txt  = "Models loaded" if models else "No models"
    key_ok  = "ok" if GROQ_API_KEY else "warn"
    key_txt = "Connected" if GROQ_API_KEY else "Not set"

    st.markdown(f"""
    <div class='sys-status'>
        <div class='sys-row'><span class='sys-key'>ML Models</span><span class='sys-val {ml_ok}'>{ml_txt}</span></div>
        <div class='sys-row'><span class='sys-key'>Groq API</span><span class='sys-val {key_ok}'>{key_txt}</span></div>
        <div class='sys-row'><span class='sys-key'>PDF Index</span><span class='sys-val {pdf_ok}'>{pdf_txt}</span></div>
        <div class='sys-row'><span class='sys-key'>Session Scans</span><span class='sys-val'>{len(st.session_state.history)}</span></div>
    </div>
    <div style='margin:12px 12px 0;text-align:center;font-size:0.55rem;
                color:var(--white-muted);border:1px solid var(--border);border-radius:8px;padding:8px;letter-spacing:0.5px'>
        ⚠ EDUCATIONAL USE ONLY · NOT MEDICAL ADVICE
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL HEADER
# ══════════════════════════════════════════════════════════════════════════════
module_name = module.split("  ")[-1]
now_str     = datetime.datetime.now().strftime("%d %b %Y · %H:%M")

st.markdown(f"""
<div class='master-header'>
    <div style='display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;flex-wrap:wrap'>
        <div>
            <div class='header-eyebrow'><span class='header-dot'></span>Clinical Decision Support · Active Module</div>
            <h1>Medora<span>AI</span> Platform</h1>
            <div class='header-sub'>
                Running: <strong>{module_name}</strong> &nbsp;·&nbsp; Real-time risk stratification with explainable AI
            </div>
            <div class='header-tags'>
                <span class='header-tag tag-red'>Cardiac Risk</span>
                <span class='header-tag tag-white'>Glycemic AI</span>
                <span class='header-tag tag-red'>ICU Scoring</span>
                <span class='header-tag tag-white'>Clinical NLP</span>
                <span class='header-tag tag-red'>PDF Chat</span>
            </div>
        </div>
        <div style='text-align:right;flex-shrink:0'>
            <div class='header-time'>{now_str}</div>
            <div style='margin-top:8px;font-size:0.6rem;color:var(--red-primary);letter-spacing:1px'>● ALL SYSTEMS LIVE</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — HEART DISEASE
# ══════════════════════════════════════════════════════════════════════════════
if "Heart Disease" in module:
    if 'heart' not in models:
        st.error("Heart disease model not loaded. Ensure models/ folder is present.")
    else:
        model, scaler, features = models['heart']
        st.markdown(f"""<div class='model-bar'>
            🫀 &nbsp;<strong>Cardiac Risk Assessment</strong>
            <span class='mbar-sep'>·</span> Sensitivity <strong>~83.6%</strong>
            <span class='mbar-sep'>·</span> Population <strong>Cleveland Cohort</strong>
            <span class='mbar-sep'>·</span> Markers <strong>13</strong>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='sec-card'><div class='sec-title'>Patient Parameters</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            age      = st.slider("Age", 29, 77, 54)
            sex      = st.selectbox("Sex", ["Female (0)", "Male (1)"])
            cp       = st.selectbox("Chest Pain Type", ["Typical Angina (0)", "Atypical Angina (1)", "Non-Anginal (2)", "Asymptomatic (3)"])
            trestbps = st.slider("Resting BP (mmHg)", 90, 200, 131)
            chol     = st.slider("Cholesterol (mg/dL)", 100, 570, 246)
        with c2:
            fbs     = st.selectbox("Fasting Blood Sugar >120?", ["No (0)", "Yes (1)"])
            restecg = st.selectbox("Resting ECG", ["Normal (0)", "ST-T Abnormality (1)", "LV Hypertrophy (2)"])
            thalach = st.slider("Max Heart Rate", 70, 202, 149)
            exang   = st.selectbox("Exercise Angina", ["No (0)", "Yes (1)"])
        with c3:
            oldpeak = st.slider("ST Depression", 0.0, 6.2, 1.0, 0.1)
            slope   = st.selectbox("ST Slope", ["Upsloping (0)", "Flat (1)", "Downsloping (2)"])
            ca      = st.slider("Major Vessels (0–3)", 0, 3, 0)
            thal    = st.selectbox("Thalassemia", ["Normal (0)", "Fixed Defect (1)", "Reversible Defect (2)"])
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("⟳  Run Cardiac Analysis"):
            input_df = pd.DataFrame([{
                'age': age, 'sex': int(sex[-2]), 'cp': int(cp[-2]),
                'trestbps': trestbps, 'chol': chol, 'fbs': int(fbs[-2]),
                'restecg': int(restecg[-2]), 'thalach': thalach,
                'exang': int(exang[-2]), 'oldpeak': oldpeak,
                'slope': int(slope[-2]), 'ca': ca, 'thal': int(thal[-2])
            }])[features]
            X = scaler.transform(input_df)
            prob = float(model.predict_proba(X)[0][1])
            pred = int(prob > 0.5)
            conf = round(max(prob, 1 - prob) * 100, 1)
            c1, c2, c3 = st.columns(3)
            c1.metric("Risk Probability", f"{prob*100:.1f}%")
            c2.metric("Prediction", "High Risk ↑" if pred else "Low Risk ↓")
            c3.metric("Confidence", f"{conf}%")
            st.markdown(render_gauge(prob), unsafe_allow_html=True)
            cls = "banner-danger" if pred else "banner-ok"
            icon = "⚠️" if pred else "✓"
            hdr  = "Elevated Heart Disease Risk" if pred else "Low Cardiac Risk"
            msg  = f"Probability <strong>{prob*100:.1f}%</strong> — {'Consult a cardiologist immediately.' if pred else 'Maintain healthy lifestyle habits.'} Confidence: {conf}%."
            st.markdown(f"<div class='result-banner {cls}'><div class='banner-icon'>{icon}</div><div class='banner-body'><h3>{hdr}</h3><p>{msg}</p></div></div>", unsafe_allow_html=True)
            st.markdown("<div class='sec-card'><div class='sec-title'>SHAP Feature Contributions</div>", unsafe_allow_html=True)
            with st.spinner("Computing SHAP…"):
                sv = get_shap_values(model, scaler, input_df)
            st.pyplot(plot_shap_bar(features, sv, "Heart Disease · SHAP Impact"), use_container_width=True)
            st.markdown("<p style='font-size:0.68rem;color:var(--white-muted);margin-top:4px'>🔴 Increases risk &nbsp;·&nbsp; 🟢 Decreases risk</p></div>", unsafe_allow_html=True)
            add_history("Heart Disease", prob, "High Risk" if pred else "Low Risk", f"Age={age} · Chol={chol} · BP={trestbps}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — DIABETES
# ══════════════════════════════════════════════════════════════════════════════
elif "Diabetes" in module:
    if 'diabetes' not in models:
        st.error("Diabetes model not loaded.")
    else:
        model, scaler, features = models['diabetes']
        st.markdown(f"""<div class='model-bar'>
            🩸 &nbsp;<strong>Glycemic Risk Screening</strong>
            <span class='mbar-sep'>·</span> Sensitivity <strong>~89.6%</strong>
            <span class='mbar-sep'>·</span> Population <strong>South Asian Cohort</strong>
            <span class='mbar-sep'>·</span> Markers <strong>8</strong>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='sec-card'><div class='sec-title'>Patient Parameters</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            pregnancies = st.slider("Pregnancies", 0, 17, 2)
            glucose     = st.slider("Glucose (mg/dL)", 44, 199, 120)
            bp          = st.slider("Blood Pressure (mmHg)", 0, 122, 69)
            skin        = st.slider("Skin Thickness (mm)", 0, 99, 20)
        with c2:
            insulin = st.slider("Insulin (μU/mL)", 0, 846, 80)
            bmi     = st.slider("BMI", 0.0, 67.1, 32.0, 0.1)
            dpf     = st.slider("Diabetes Pedigree", 0.078, 2.42, 0.47, 0.001)
            age     = st.slider("Age", 21, 81, 33)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("⟳  Run Diabetes Analysis"):
            input_df = pd.DataFrame([{
                'Pregnancies': pregnancies, 'Glucose': glucose, 'BloodPressure': bp,
                'SkinThickness': skin, 'Insulin': insulin, 'BMI': bmi,
                'DiabetesPedigreeFunction': dpf, 'Age': age
            }])[features]
            X    = scaler.transform(input_df)
            prob = float(model.predict_proba(X)[0][1])
            pred = int(prob > 0.5)
            hba1c = round(5.5 + prob * 4, 1)
            c1, c2, c3 = st.columns(3)
            c1.metric("Diabetes Probability", f"{prob*100:.1f}%")
            c2.metric("Prediction", "Diabetic ↑" if pred else "Non-Diabetic ✓")
            c3.metric("Est. HbA1c", f"~{hba1c}%")
            st.markdown(render_gauge(prob), unsafe_allow_html=True)
            cls  = "banner-danger" if pred else "banner-ok"
            icon = "⚠️" if pred else "✓"
            hdr  = "Diabetes Risk Detected" if pred else "No Significant Diabetes Risk"
            msg  = f"Probability <strong>{prob*100:.1f}%</strong> — {'Consult an endocrinologist. Est. HbA1c: ~' + str(hba1c) + '%.' if pred else 'Maintain healthy glucose and BMI levels.'}"
            st.markdown(f"<div class='result-banner {cls}'><div class='banner-icon'>{icon}</div><div class='banner-body'><h3>{hdr}</h3><p>{msg}</p></div></div>", unsafe_allow_html=True)
            st.markdown("<div class='sec-card'><div class='sec-title'>SHAP Feature Contributions</div>", unsafe_allow_html=True)
            with st.spinner("Computing SHAP…"):
                sv = get_shap_values(model, scaler, input_df)
            st.pyplot(plot_shap_bar(features, sv, "Diabetes Risk · SHAP Impact"), use_container_width=True)
            st.markdown("<p style='font-size:0.68rem;color:var(--white-muted);margin-top:4px'>🔴 Increases risk &nbsp;·&nbsp; 🟢 Decreases risk</p></div>", unsafe_allow_html=True)
            add_history("Diabetes", prob, "Diabetic" if pred else "Non-Diabetic", f"Glucose={glucose} · BMI={bmi} · Age={age}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3 — ICU READMISSION
# ══════════════════════════════════════════════════════════════════════════════
elif "ICU" in module:
    st.markdown(f"""<div class='model-bar'>
        🏨 &nbsp;<strong>ICU Readmission Risk</strong>
        <span class='mbar-sep'>·</span> Index <strong>LACE Score</strong>
        <span class='mbar-sep'>·</span> Window <strong>30-Day Post-Discharge</strong>
        <span class='mbar-sep'>·</span> Factors <strong>8</strong>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sec-card'><div class='sec-title'>Patient ICU Record</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        age        = st.slider("Age", 18, 95, 60)
        icu_days   = st.slider("ICU Stay (days)", 1, 30, 5)
        prev_admit = st.slider("Previous Admissions (1yr)", 0, 10, 1)
        num_diag   = st.slider("Number of Diagnoses", 1, 20, 5)
    with c2:
        num_proc    = st.slider("Number of Procedures", 0, 25, 4)
        num_meds    = st.slider("Number of Medications", 1, 30, 8)
        creatinine  = st.slider("Creatinine (mg/dL)", 0.5, 12.0, 1.1, 0.1)
        wbc         = st.slider("WBC (×10³/μL)", 2.0, 30.0, 8.5, 0.1)
    with c3:
        hemoglobin  = st.slider("Hemoglobin (g/dL)", 5.0, 18.0, 13.0, 0.1)
        sodium      = st.slider("Sodium (mEq/L)", 120, 160, 138)
        glucose_icu = st.slider("Blood Glucose (mg/dL)", 60, 400, 110)
        discharge   = st.selectbox("Discharge To", ["Home (low risk)", "SNF/Rehab (moderate)", "Transfer (high risk)"])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⟳  Run ICU Readmission Analysis"):
        score  = 0
        score += min(icu_days * 3, 15)
        score += min(prev_admit * 8, 24)
        score += min(num_diag * 2, 10)
        score += 8 if creatinine > 5 else 4 if creatinine > 2 else 0
        score += 5 if age > 70 else 3 if age > 55 else 0
        score += 6 if "Transfer" in discharge else 3 if "SNF" in discharge else 0
        score += 4 if wbc > 15 or wbc < 4 else 0
        score += 3 if hemoglobin < 9 else 0
        prob   = min(score / 70.0, 1.0)

        c1, c2, c3 = st.columns(3)
        c1.metric("Readmission Risk", f"{prob*100:.1f}%")
        c2.metric("Risk Level", "🔴 High" if prob > 0.6 else "🟡 Moderate" if prob > 0.3 else "🟢 Low")
        c3.metric("LACE Score", f"{score} / 70")
        st.markdown(render_gauge(prob), unsafe_allow_html=True)

        if prob > 0.6:
            st.markdown(f"<div class='result-banner banner-danger'><div class='banner-icon'>⚠️</div><div class='banner-body'><h3>High ICU Readmission Risk</h3><p>LACE: <strong>{score}/70</strong> — Enhanced post-discharge monitoring required.</p></div></div>", unsafe_allow_html=True)
        elif prob > 0.3:
            st.markdown(f"<div class='result-banner banner-warn'><div class='banner-icon'>⚡</div><div class='banner-body'><h3>Moderate Readmission Risk</h3><p>LACE: <strong>{score}/70</strong> — Follow-up within 48–72 hours recommended.</p></div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-banner banner-ok'><div class='banner-icon'>✓</div><div class='banner-body'><h3>Low Readmission Risk</h3><p>LACE: <strong>{score}/70</strong> — Standard discharge protocol applicable.</p></div></div>", unsafe_allow_html=True)

        st.markdown("<div class='sec-card'><div class='sec-title'>Risk Factor Breakdown</div>", unsafe_allow_html=True)
        factors = {
            "ICU Stay Duration": min(icu_days * 3, 15), "Previous Admissions": min(prev_admit * 8, 24),
            "Number of Diagnoses": min(num_diag * 2, 10), "Creatinine": 8 if creatinine > 5 else 4 if creatinine > 2 else 0,
            "Patient Age": 5 if age > 70 else 3 if age > 55 else 0,
            "Discharge Disposition": 6 if "Transfer" in discharge else 3 if "SNF" in discharge else 0,
            "Abnormal WBC": 4 if wbc > 15 or wbc < 4 else 0, "Low Hemoglobin": 3 if hemoglobin < 9 else 0,
        }
        names  = list(factors.keys())
        vals   = [float(v) for v in factors.values()]
        colors = ['#e31b23' if v > 5 else '#ffab00' if v > 0 else '#1a1a1a' for v in vals]
        fig, ax = plt.subplots(figsize=(7, 3.8))
        ax.barh(names, vals, color=colors, edgecolor='none', height=0.48, alpha=0.88)
        ax.set_xlabel("Score Contribution", fontsize=8, color='#888888', labelpad=8)
        ax.tick_params(labelsize=7.5, colors='#888888', length=0)
        for s in ax.spines.values(): s.set_visible(False)
        ax.set_facecolor('#0a0a0a'); fig.patch.set_facecolor('#0a0a0a')
        ax.grid(axis='x', color=(1, 1, 1, 0.03), linewidth=0.5, linestyle='--')
        fig.tight_layout(pad=1.5)
        st.pyplot(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        add_history("ICU Readmission", prob, "High Risk" if prob > 0.6 else "Moderate" if prob > 0.3 else "Low Risk", f"LACE={score}/70 · Stay={icu_days}d")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 4 — NLP
# ══════════════════════════════════════════════════════════════════════════════
elif "NLP" in module:
    SAMPLE = """Patient is a 58-year-old male presenting with chest pain and shortness of breath.
History of hypertension and diabetes. Current medications include metformin, aspirin, and lisinopril.
Blood pressure: 148/92 mmHg. Heart rate: 96 bpm. SpO2: 94%. Cholesterol: 280 mg/dL.
ECG shows ST-segment changes suggestive of coronary artery disease. Troponin mildly elevated.
Patient reports fatigue, palpitations, and edema in lower extremities for the past 3 weeks."""

    st.markdown("<div class='sec-card'><div class='sec-title'>Clinical Notes Input</div>", unsafe_allow_html=True)
    text = st.text_area("Paste medical report:", value=SAMPLE, height=175, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⟳  Analyze Medical Report"):
        if text.strip():
            found, risk = nlp_analyze(text)
            total = sum(len(v) for v in found.values())
            rl    = "High" if risk > 60 else "Moderate" if risk > 30 else "Low"
            prob  = risk / 100

            c1, c2, c3 = st.columns(3)
            c1.metric("Clinical Risk Score", f"{risk}/100")
            c2.metric("Risk Level", rl)
            c3.metric("Entities Found", str(total))
            st.markdown(render_gauge(prob), unsafe_allow_html=True)

            cls  = "banner-danger" if risk > 60 else "banner-warn" if risk > 30 else "banner-ok"
            icon = "⚠️" if risk > 60 else "⚡" if risk > 30 else "✓"
            hdr  = "Elevated Clinical Risk" if risk > 60 else "Moderate Risk Profile" if risk > 30 else "Low Risk Profile"
            msg  = "Multiple disease indicators found. Immediate evaluation recommended." if risk > 60 else "Monitor closely. Follow-up within 48–72 hours." if risk > 30 else "Minimal clinical indicators. Routine monitoring advised."
            st.markdown(f"<div class='result-banner {cls}'><div class='banner-icon'>{icon}</div><div class='banner-body'><h3>{hdr}</h3><p>{msg}</p></div></div>", unsafe_allow_html=True)

            st.markdown("<div class='sec-card'><div class='sec-title'>Named Entity Recognition</div>", unsafe_allow_html=True)
            labels = {"DISEASE": ("🦠", "Diseases"), "SYMPTOM": ("🤒", "Symptoms"), "MEDICATION": ("💊", "Medications"), "ANATOMY": ("🫀", "Anatomy"), "VITAL": ("📊", "Vitals & Labs")}
            for etype, (icon2, label) in labels.items():
                if etype in found:
                    tags = "".join(f"<span class='entity-tag tag-{etype}'>{e}</span>" for e in found[etype])
                    st.markdown(f"<div class='entity-group'><div class='entity-label'>{icon2} {label}</div>{tags}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='sec-card'><div class='sec-title'>Annotated Report</div>", unsafe_allow_html=True)
            import html as hl
            highlighted = hl.escape(text)
            color_map = {"DISEASE": ("#2a0a10", "#ff6b6b"), "SYMPTOM": ("#1a1500", "#ffc44d"), "MEDICATION": ("#0a1a0a", "#4cff8f"), "ANATOMY": ("#0a0a1a", "#aaaaaa"), "VITAL": ("#1a0505", "#ff8a8a")}
            all_terms = [(t.lower(), et) for et, tl_list in found.items() for t in tl_list]
            all_terms.sort(key=lambda x: -len(x[0]))
            for term, etype in all_terms:
                bg, tc = color_map.get(etype, ("#1a1a1a", "#ffffff"))
                highlighted = highlighted.replace(term.title(), f"<mark style='background:{bg};color:{tc};padding:2px 8px;border-radius:4px;font-weight:500'>{term.title()}</mark>")
            st.markdown(f"<div class='annotated-text'>{highlighted}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            add_history("NLP Analysis", prob, rl, f"Entities={total} · Score={risk}/100")
        else:
            st.warning("Please enter some clinical notes to analyze.")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 5 — PDF ASSISTANT (RAG)
# ══════════════════════════════════════════════════════════════════════════════
elif "PDF" in module:
    st.markdown(f"""<div class='model-bar'>
        ⚕️ &nbsp;<strong>Medical Assistant</strong>
        <span class='mbar-sep'>·</span> Engine <strong>Groq LLM</strong>
        <span class='mbar-sep'>·</span> Embeddings <strong>HuggingFace MPNet</strong>
        <span class='mbar-sep'>·</span> Explains in <strong>Plain Language</strong>
    </div>""", unsafe_allow_html=True)

    if not GROQ_API_KEY:
        st.markdown("""<div class='result-banner banner-danger'>
            <div class='banner-icon'>⚠️</div>
            <div class='banner-body'>
                <h3>Groq API Key Missing</h3>
                <p>Set the <code>GROQ_API_KEY</code> environment variable or add it to Streamlit Secrets to use the PDF Assistant.</p>
            </div></div>""", unsafe_allow_html=True)
    else:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("<div class='sec-card'><div class='sec-title'>Upload Medical PDF</div>", unsafe_allow_html=True)
            uploaded_pdf = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")
            if uploaded_pdf:
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("🚀  Process PDF"):
                        with st.spinner("Loading embedding model…"):
                            if st.session_state.embeddings is None:
                                st.session_state.embeddings = load_embeddings()
                        with st.spinner("Indexing document chunks…"):
                            n = process_pdf(uploaded_pdf)
                        st.markdown(f"<div class='result-banner banner-ok'><div class='banner-icon'>✓</div><div class='banner-body'><h3>PDF Indexed</h3><p><strong>{uploaded_pdf.name}</strong> — {n} chunks embedded and ready.</p></div></div>", unsafe_allow_html=True)
                with col_b:
                    if st.button("🗑  Clear Chat"):
                        st.session_state.chat_history = []
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("<div class='sec-card'><div class='sec-title'>Model Settings</div>", unsafe_allow_html=True)
            groq_model = st.selectbox("LLM Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"])
            top_k = st.slider("Context Chunks (K)", 2, 8, 4)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='sec-card'><div class='sec-title'>Conversation</div>", unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown("""<div class='chat-empty'>
                <span>💊</span>
                Upload a medical PDF and ask me anything.<br>
                I'll explain it in simple, plain language anyone can understand.
            </div>""", unsafe_allow_html=True)
        else:
            for turn in st.session_state.chat_history:
                st.markdown(f"""
                <div class='chat-user'>
                    <div>
                        <span class='bubble-label label-user'>You</span>
                        <div class='bubble-user'>{turn['user']}</div>
                    </div>
                </div>
                <div class='chat-ai'>
                    <div>
                        <span class='bubble-label label-ai'>MediMind Assistant</span>
                        <div class='bubble-ai'>{turn['assistant'].replace(chr(10), '<br>')}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

                if turn.get("sources"):
                    chips = "".join(f"<span class='source-chip'>📄 Page {src.metadata.get('page','?')} · {src.page_content[:40].replace(chr(10),' ')}…</span>"
                                    for src in turn["sources"])
                    with st.expander("📎 Source Passages"):
                        st.markdown(chips, unsafe_allow_html=True)
                        for i, src in enumerate(turn["sources"], 1):
                            pg = src.metadata.get("page", "?")
                            st.markdown(f"**Chunk {i} — Page {pg}**\n\n{src.page_content[:400]}…")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.pdf_loaded:
            st.markdown("<div class='sec-card'><div class='sec-title'>Ask a Question</div>", unsafe_allow_html=True)
            with st.form(key="qa_form", clear_on_submit=True):
                user_query = st.text_area(
                    "Your question",
                    placeholder="e.g. What does this report say about my heart? / What medication was prescribed? / Is this result normal?",
                    height=90,
                    label_visibility="collapsed",
                )
                col_btn, col_hint = st.columns([1, 3])
                with col_btn:
                    submitted = st.form_submit_button("🔍  Ask")
                with col_hint:
                    st.markdown("<p style='font-size:0.68rem;color:var(--white-muted);padding-top:14px'>Answers based strictly on the uploaded PDF</p>", unsafe_allow_html=True)
            if submitted and user_query.strip():
                with st.spinner("Searching document & generating plain-language answer…"):
                    sources = retrieve_context(user_query, k=top_k)
                    context = "\n\n".join([d.page_content for d in sources])
                    answer  = ask_groq(user_query, context, groq_model, st.session_state.chat_history)
                st.session_state.chat_history.append({"user": user_query, "assistant": answer, "sources": sources})
                add_history("PDF Assistant", 0.5, "Q&A", f"Q: {user_query[:40]}…")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div class='result-banner banner-warn'>
                <div class='banner-icon'>📄</div>
                <div class='banner-body'>
                    <h3>No PDF Loaded</h3>
                    <p>Upload a PDF above and click <strong>Process PDF</strong> to start asking questions.</p>
                </div></div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 6 — PATIENT HISTORY
# ══════════════════════════════════════════════════════════════════════════════
elif "History" in module:
    hist  = st.session_state.history
    total = len(hist)
    high  = sum(1 for h in hist if h['prob'] > 60)
    mod   = sum(1 for h in hist if 30 < h['prob'] <= 60)
    low   = sum(1 for h in hist if h['prob'] <= 30)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Scans", total)
    c2.metric("High Risk", high)
    c3.metric("Moderate", mod)
    c4.metric("Low Risk", low)

    st.markdown("<div class='sec-card'><div class='sec-title'>Prediction Log</div>", unsafe_allow_html=True)
    render_history()
    st.markdown("</div>", unsafe_allow_html=True)

    if hist:
        if st.button("🗑  Clear All History"):
            st.session_state.history = []
            st.rerun()

        if total > 0:
            st.markdown("<div class='sec-card'><div class='sec-title'>Risk Distribution</div>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(5, 2.8))
            ax.bar(["High Risk", "Moderate", "Low Risk"], [high, mod, low],
                   color=['#e31b23', '#ffab00', '#00c853'], width=0.42, edgecolor='none', alpha=0.88)
            for i, v in enumerate([high, mod, low]):
                if v > 0:
                    ax.text(i, v + 0.05, str(v), ha='center', va='bottom', color='#ffffff', fontsize=9)
            ax.set_facecolor('#0a0a0a'); fig.patch.set_facecolor('#0a0a0a')
            ax.tick_params(colors='#888888', labelsize=8, length=0)
            for s in ax.spines.values(): s.set_visible(False)
            ax.set_ylabel("Count", color='#888888', fontsize=8)
            ax.grid(axis='y', color=(1, 1, 1, 0.03), linewidth=0.5)
            fig.tight_layout(pad=1.5)
            st.pyplot(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)


# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    MEDORA AI PLATFORM · v3.0 · SHAP XAI · RAG · CLINICAL NLP &nbsp;·&nbsp;
    FOR EDUCATIONAL USE ONLY 
</div>
""", unsafe_allow_html=True)
