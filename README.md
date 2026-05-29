# 🔍 Room Inspector

Détection d'objets et d'anomalies dans une salle, propulsé par **Groq Vision + Llama 4 Scout**.

## 🚀 Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Pour que la clé API soit chargée automatiquement en local, crée un fichier `.streamlit/secrets.toml` :

```toml
GROQ_API_KEY = "gsk_..."
```

Ou définis la variable d'environnement :

```bash
export GROQ_API_KEY="gsk_..."
streamlit run app.py
```

## ☁️ Déploiement Streamlit Cloud

1. Fork ce repo sur GitHub
2. Va sur [share.streamlit.io](https://share.streamlit.io)
3. Connecte ton compte GitHub
4. Sélectionne ce repo → `app.py`
5. Dans **Secrets**, ajoute : `GROQ_API_KEY = "gsk_..."`
6. Clique **Deploy** → URL publique générée, **aucune saisie de clé requise** !

## 🔑 Obtenir une clé API Groq (gratuite)

1. Va sur [console.groq.com/keys](https://console.groq.com/keys)
2. Connecte-toi avec Google ou GitHub
3. Clique **Create API key**
4. Colle la clé dans `.streamlit/secrets.toml` (voir ci-dessus)
