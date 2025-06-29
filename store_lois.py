import re
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from constants import *

def chunk_by_article(text, loi_name):
    """
    Découpe le texte en chunks selon les articles et ajoute la métadonnée de la loi.
    :param text: texte complet
    :param loi_name: nom de la loi (ex: 'Code Civil')
    :return: liste de dicts [{content, metadata}]
    """
    pattern = r"(Article\s+\d+\w*\.|Art\.\s*\d+\w*\.)"
    splits = re.split(pattern, text)
    chunks = []

    for i in range(1, len(splits), 2):
        title = splits[i].strip()
        content = splits[i + 1].strip() if (i + 1) < len(splits) else ""
        full_content = f"{title}\n{content}"

        chunks.append({
            "content": full_content,
            "metadata": {
                "loi": loi_name,
                "article": title
            }
        })

    return chunks

def init_qdrant():
    client = QdrantClient(QDRANT_URL, api_key=QDRANT_API)
    embedding_model = HuggingFaceEmbeddings(model_name=MODEL_EMBEDDING)
    vector_size = embedding_model.client.get_sentence_embedding_dimension()

    if not client.collection_exists(QDRANT_COLLECTION):
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    vectorstore = Qdrant(
        client=client,
        collection_name=QDRANT_COLLECTION,
        embeddings=embedding_model
    )
    return client, embedding_model, vectorstore

# ⚡ Initialisation Qdrant et Embedding
client, embedding_model, vectorstore = init_qdrant()

# ⚡ Lecture du fichier texte
with open("output/code_penal_extrait_clean.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

# ⚡ Chunking par article
chunks = chunk_by_article(full_text, "Code Penal")

# ⚡ Upload des textes et métadonnées via LangChain
texts = [chunk["content"] for chunk in chunks]
metadatas = [chunk["metadata"] for chunk in chunks]

vectorstore.add_texts(texts=texts, metadatas=metadatas)

print(f"✅ {len(texts)} articles insérés dans la collection '{QDRANT_COLLECTION}' avec succès.")
