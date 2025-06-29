from qdrant_client import QdrantClient
from constants import QDRANT_URL, QDRANT_API, QDRANT_COLLECTION

# 🔧 Initialisation du client Qdrant
client = QdrantClient(QDRANT_URL, api_key=QDRANT_API)

# 🚨 Suppression de la collection
client.delete_collection(collection_name=QDRANT_COLLECTION)

print(f"✅ La collection '{QDRANT_COLLECTION}' a été supprimée avec succès.")
