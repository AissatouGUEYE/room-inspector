import streamlit as st
import requests
import json
import re
import base64
from PIL import Image
import io

st.set_page_config(
    page_title="Room Inspector",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: linear-gradient(160deg, #EEF4FF 0%, #F7F9FF 60%, #EEF4FF 100%);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 1rem 4rem; max-width: 430px; margin: auto; }

/* HEADER */
.ri-header { text-align: center; padding: 32px 24px 24px; }
.ri-logo {
    width: 68px; height: 68px;
    background: linear-gradient(135deg, #1A56DB 0%, #3B82F6 100%);
    border-radius: 22px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; margin: 0 auto 16px;
    box-shadow: 0 8px 24px rgba(26,86,219,0.30);
}
.ri-title { font-size: 26px; font-weight: 700; color: #0D1B4B; margin: 0 0 6px; letter-spacing: -0.5px; }
.ri-subtitle { font-size: 13px; color: #6B7BB0; margin: 0; }

/* PILL */
.pill {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 6px 16px; border-radius: 100px;
    font-size: 12px; font-weight: 600;
    margin: 0 auto 20px;
}
.pill-ok  { background: #EEF4FF; color: #1A56DB; border: 1px solid #BFCFFA; }
.pill-err { background: #FEF0F0; color: #C0392B; border: 1px solid #FACACA; }
.pill-dot { width: 7px; height: 7px; border-radius: 50%; }
.pill-ok  .pill-dot { background: #1A56DB; box-shadow: 0 0 0 3px #BFCFFA; animation: pulse 2s infinite; }
.pill-err .pill-dot { background: #E74C3C; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* CARD */
.card {
    background: white;
    border-radius: 20px; padding: 20px;
    margin-bottom: 14px;
    border: 1px solid #E0E8FF;
    box-shadow: 0 2px 16px rgba(26,86,219,0.06);
}
.card-title {
    font-size: 11px; font-weight: 700; color: #6B7BB0;
    letter-spacing: 0.8px; text-transform: uppercase; margin: 0 0 14px;
}

/* SCORE */
.score-wrap { display: flex; align-items: center; gap: 18px; }
.score-ring {
    flex-shrink: 0; width: 84px; height: 84px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-direction: column; font-size: 26px; font-weight: 700;
}
.score-ring small { font-size: 11px; font-weight: 500; opacity: 0.7; margin-top: -2px; }
.score-resume { font-size: 13px; color: #3D4F7C; line-height: 1.6; flex: 1; }

/* METRICS */
.metrics-row { display: flex; gap: 10px; margin-bottom: 14px; }
.metric-card {
    flex: 1; background: #F0F5FF; border-radius: 16px;
    padding: 14px 10px; text-align: center; border: 1px solid #D6E4FF;
}
.metric-val { font-size: 28px; font-weight: 700; line-height: 1; }
.metric-lbl { font-size: 11px; color: #6B7BB0; margin-top: 4px; font-weight: 600; }

/* CHIPS */
.chips-wrap { display: flex; flex-wrap: wrap; gap: 8px; }
.chip {
    background: #EEF4FF; border: 1px solid #BFCFFA;
    border-radius: 100px; padding: 7px 14px;
    font-size: 13px; color: #1A3DAA;
    display: inline-flex; align-items: center; gap: 6px; font-weight: 500;
}

/* ANOMALIE */
.an-card {
    border-radius: 14px; padding: 13px 15px;
    margin-bottom: 9px; display: flex; gap: 12px; align-items: flex-start;
}
.an-haute   { background:#FEF0F0; border:1px solid #FACACA; }
.an-moyenne { background:#FFFBEB; border:1px solid #FDE68A; }
.an-basse   { background:#EEF4FF; border:1px solid #BFCFFA; }
.an-icon { font-size: 18px; margin-top:1px; }
.an-badge {
    display:inline-block; font-size:10px; font-weight:700;
    padding:2px 8px; border-radius:100px; margin-bottom:5px;
    letter-spacing:0.4px; text-transform:uppercase;
}
.badge-haute   { background:#FEE2E2; color:#991B1B; }
.badge-moyenne { background:#FEF3C7; color:#92400E; }
.badge-basse   { background:#EEF4FF; color:#1A56DB; }
.an-title { font-size:13px; font-weight:700; color:#0D1B4B; margin-bottom:3px; }
.an-desc  { font-size:12px; color:#3D4F7C; line-height:1.5; }

/* API KEY BOX */
.key-box {
    background: #EEF4FF; border: 1px solid #BFCFFA;
    border-radius: 14px; padding: 16px;
    font-size: 13px; color: #1A3DAA; margin-bottom: 14px;
    line-height: 1.7;
}
.install-box {
    background: #0D1B4B; border-radius: 12px;
    padding: 13px 16px; font-family: monospace;
    font-size: 12px; color: #93C5FD; margin: 8px 0;
    white-space: pre-wrap; line-height: 1.6;
}

/* BUTTONS */
div.stButton > button {
    width: 100%; border-radius: 14px !important;
    font-weight: 700 !important; font-size: 15px !important;
    padding: 14px 0 !important; border: none !important;
    background: linear-gradient(135deg, #1A56DB 0%, #3B82F6 100%) !important;
    color: white !important;
    box-shadow: 0 4px 16px rgba(26,86,219,0.30) !important;
}
div.stButton > button:hover { opacity: 0.88 !important; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: #EEF4FF; border-radius: 12px; padding: 4px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important; font-weight: 600 !important;
    font-size: 13px !important; color: #6B7BB0 !important;
}
.stTabs [aria-selected="true"] {
    background: white !important; color: #1A56DB !important;
    box-shadow: 0 1px 6px rgba(26,86,219,0.12) !important;
}
</style>
""", unsafe_allow_html=True)

# ── CONFIG ─────────────────────────────────────────────────────────────────────
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL    = "meta-llama/llama-4-scout-17b-16e-instruct"   # vision gratuit sur Groq

PROMPT = """You are a professional room inspection AI. Analyze this room image carefully and thoroughly.

Respond ONLY with valid JSON, no markdown, no backticks, no explanation.

{
  "objets": [
    {"nom": "chaise", "count": 4, "emoji": "🪑"},
    {"nom": "table", "count": 1, "emoji": "🪵"},
    {"nom": "tableau blanc", "count": 1, "emoji": "📋"}
  ],
  "anomalies": [
    {"type": "chaise renversée", "severite": "haute", "description": "Une chaise est tombée près de la fenêtre côté gauche"}
  ],
  "score_proprete": 78,
  "resume": "Salle avec 4 chaises et 1 table. 1 anomalie critique détectée."
}

Rules:
- Count EVERY visible object: chairs, tables, desks, screens, projectors, whiteboards, boards, doors, windows, bags, cables, bottles, papers, trash, etc.
- Be precise with counts — look carefully at each individual item
- Anomalies: overturned/fallen objects, clutter, floor obstacles, open doors/windows, damaged equipment, stains, cables on floor, displaced items
- Severity: "haute"=safety/urgent, "moyenne"=functional issue, "basse"=aesthetic only
- score_proprete 0-100 (90+=perfect, 70-89=good, 50-69=average, <50=bad)
- No anomalies → "anomalies": []
- JSON ONLY — nothing else before or after"""


def resize(img, max_px=1024):
    w, h = img.size
    if max(w, h) > max_px:
        r = max_px / max(w, h)
        img = img.resize((int(w*r), int(h*r)), Image.LANCZOS)
    return img

def pil_to_b64(img):
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()

def analyser(api_key, img):
    img  = resize(img)
    b64  = pil_to_b64(img)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text", "text": PROMPT}
            ]
        }],
        "temperature": 0.05,
        "max_tokens": 1024
    }
    resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    raw   = resp.json()["choices"][0]["message"]["content"].strip()
    clean = re.sub(r"```json|```", "", raw).strip()
    match = re.search(r'\{.*\}', clean, re.DOTALL)
    if not match:
        raise ValueError(f"Pas de JSON : {raw[:300]}")
    return json.loads(match.group())

def score_style(s):
    if s >= 80: return "#065F46", "#ECFDF5", "#BBF7D0"
    if s >= 50: return "#92400E", "#FFFBEB", "#FDE68A"
    return "#991B1B", "#FEF2F2", "#FECACA"

def sev_icon(s):
    return {"haute":"🔴","moyenne":"🟡","basse":"🔵"}.get(s,"⚪")

def sev_label(s):
    return {"haute":"Critique","moyenne":"Moyen","basse":"Mineur"}.get(s,s)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ri-header">
  <div class="ri-logo">🔍</div>
  <h1 class="ri-title">Room Inspector</h1>
  <p class="ri-subtitle">Détection d'objets & anomalies · Groq Vision · Gratuit</p>
</div>
""", unsafe_allow_html=True)

# ── CLÉ API ────────────────────────────────────────────────────────────────────
# Priorité : 1) session, 2) secrets Streamlit, 3) variable d'environnement
import os
if "groq_key" not in st.session_state:
    try:
        st.session_state["groq_key"] = st.secrets["GROQ_API_KEY"]
    except Exception:
        env_key = os.environ.get("GROQ_API_KEY", "")
        if env_key:
            st.session_state["groq_key"] = env_key

# N'afficher le formulaire que si aucune clé n'a été trouvée automatiquement
if "groq_key" not in st.session_state:
    with st.expander("🔑 Clé API Groq", expanded=True):
        st.markdown("""
        <div class="key-box">
          1. Va sur <strong>console.groq.com/keys</strong><br>
          2. Connecte-toi avec Google / GitHub (gratuit)<br>
          3. Clique <strong>Create API key</strong><br>
          4. Colle la clé ici 👇 (commence par <code>gsk_...</code>)
        </div>
        """, unsafe_allow_html=True)
        key_input = st.text_input("Clé API Groq", type="password",
                                   placeholder="gsk_...",
                                   value="")
        if st.button("💾 Enregistrer"):
            if len(key_input) > 10:
                st.session_state["groq_key"] = key_input
                st.success("✅ Clé enregistrée !")
                st.rerun()
            else:
                st.error("Clé trop courte.")

if "groq_key" not in st.session_state:
    st.markdown("""
    <div style="text-align:center">
      <div class="pill pill-err"><span class="pill-dot"></span> Clé API manquante</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

st.markdown("""
<div style="text-align:center">
  <div class="pill pill-ok"><span class="pill-dot"></span> Groq Vision · Llama 4 Scout · Prêt</div>
</div>""", unsafe_allow_html=True)

# ── CAPTURE ────────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">📷 Photo de la salle</div>', unsafe_allow_html=True)
tab_cam, tab_file = st.tabs(["📷  Caméra", "🖼  Fichier"])
uploaded = None
with tab_cam:
    cam = st.camera_input(" ", label_visibility="collapsed")
    if cam: uploaded = cam
with tab_file:
    fil = st.file_uploader(" ", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
    if fil: uploaded = fil
st.markdown("</div>", unsafe_allow_html=True)

# ── ANALYSE ────────────────────────────────────────────────────────────────────
if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_container_width=True, caption="")

    if st.button("🔍  Analyser la salle"):
        with st.spinner("Groq analyse la salle… (~3 secondes)"):
            try:
                result = analyser(st.session_state["groq_key"], img)
                st.session_state["result"] = result
                st.rerun()
            except json.JSONDecodeError as e:
                st.error(f"Réponse non parsable — réessaie. ({e})")
                st.stop()
            except requests.HTTPError as e:
                code = e.response.status_code if e.response else 0
                if code == 401:
                    st.error("❌ Clé API invalide. Vérifie sur console.groq.com/keys")
                elif code == 429:
                    st.error("⏳ Quota atteint. Attends 1 minute et réessaie.")
                else:
                    st.error(f"Erreur HTTP {code} : {e}")
                st.stop()
            except Exception as e:
                st.error(f"Erreur : {e}")
                st.stop()

# ── RÉSULTATS ──────────────────────────────────────────────────────────────────
if "result" in st.session_state:
    r     = st.session_state["result"]
    score = r.get("score_proprete", 0)
    n_an  = len(r.get("anomalies", []))
    n_obj = sum(o.get("count", 1) for o in r.get("objets", []))
    tc, bg, brd = score_style(score)

    # Score + résumé
    st.markdown(f"""
    <div class="card">
      <div class="card-title">Résultat global</div>
      <div class="score-wrap">
        <div class="score-ring" style="background:{bg};border:3px solid {brd};color:{tc}">
          {score}<small>/100</small>
        </div>
        <div class="score-resume">{r.get("resume","")}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Métriques
    ac = "#991B1B" if n_an > 0 else "#065F46"
    st.markdown(f"""
    <div class="metrics-row">
      <div class="metric-card">
        <div class="metric-val" style="color:{tc}">{score}</div>
        <div class="metric-lbl">Propreté</div>
      </div>
      <div class="metric-card">
        <div class="metric-val" style="color:#1A56DB">{n_obj}</div>
        <div class="metric-lbl">Objets</div>
      </div>
      <div class="metric-card">
        <div class="metric-val" style="color:{ac}">{n_an}</div>
        <div class="metric-lbl">Anomalies</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Objets
    if r.get("objets"):
        chips = "".join(
            f'<span class="chip">{o.get("emoji","📦")} {o["nom"].capitalize()} × {o["count"]}</span>'
            for o in r["objets"]
        )
        st.markdown(f"""
        <div class="card">
          <div class="card-title">Objets détectés</div>
          <div class="chips-wrap">{chips}</div>
        </div>""", unsafe_allow_html=True)

    # Anomalies
    anomalies = r.get("anomalies", [])
    if not anomalies:
        st.markdown("""
        <div class="card" style="text-align:center;padding:28px">
          <div style="font-size:36px;margin-bottom:10px">✅</div>
          <div style="font-size:15px;font-weight:700;color:#065F46">Aucune anomalie détectée</div>
          <div style="font-size:13px;color:#6B7BB0;margin-top:4px">La salle est en ordre</div>
        </div>""", unsafe_allow_html=True)
    else:
        cards_html = ""
        for a in anomalies:
            sev = a.get("severite","basse")
            cards_html += f"""
            <div class="an-card an-{sev}">
              <div class="an-icon">{sev_icon(sev)}</div>
              <div>
                <div class="an-badge badge-{sev}">{sev_label(sev)}</div>
                <div class="an-title">{a.get("type","").capitalize()}</div>
                <div class="an-desc">{a.get("description","")}</div>
              </div>
            </div>"""
        st.markdown(f'<div class="card"><div class="card-title">Anomalies détectées</div>{cards_html}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        if st.button("📷  Nouvelle photo"):
            del st.session_state["result"]
            st.rerun()
    with cb:
        if st.button("🔄  Ré-analyser"):
            del st.session_state["result"]
            st.rerun()
