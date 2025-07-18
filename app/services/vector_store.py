import os
import chromadb
from chromadb.config import Settings
from app.services import openai_client

# Initialize Chroma persistent client with a specified directory
CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
client = chromadb.PersistentClient(path=CHROMA_DIR, settings=Settings(anonymized_telemetry=False))

def get_collection(user_id: str):
    # Use a separate collection per user for isolation
    collection_name = f"docs_{user_id}"
    return client.get_or_create_collection(name=collection_name)

def add_documents(user_id: str, docs: list[str], embeddings: list[list[float]], sources: list[str]):
    collection = get_collection(user_id)
    doc_ids = [f"{user_id}_{i}" for i in range(len(docs))]
    metadatas = [{"source": source} for source in sources]
    # print(metadatas)
    collection.add(documents=docs, embeddings=embeddings, ids=doc_ids, metadatas=metadatas)
    # stored_data = collection.get()

def query_documents(user_id: str, query_text: str, top_k: int = 5) -> list[dict]:
    collection = get_collection(user_id)
    try:
        query_vector = openai_client.embed_text([query_text])[0]
        results = collection.query(query_embeddings=[query_vector], n_results=top_k)
        # print(results)
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        return [{"text": doc, "source": meta.get("source", "unknown")} for doc, meta in zip(documents, metadatas)]

    except Exception as e:
        print(f"Exception occurred: {e}")
        return []

