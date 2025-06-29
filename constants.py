
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
loaded = load_dotenv()

# Récupérer les clés API de manière sécurisée
QDRANT_API = os.getenv('QDRANT_API')
QDRANT_URL = os.getenv('QDRANT_URL')

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

QDRANT_COLLECTION = os.getenv('QDRANT_COLLECTION')

# Modèles utilisés
LLM_NAME="llama-3.3-70b-versatile"
MODEL_EMBEDDING="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
