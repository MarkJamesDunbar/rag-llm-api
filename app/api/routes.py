# app/api/routes.py
from fastapi import APIRouter, UploadFile, File, Depends
from app.services import document_loader, vector_store, openai_client, session_manager
from app.models import schemas

router = APIRouter()

@router.post("/upload_pdf", response_model=schemas.UploadResponse)
async def upload_pdf(user_id: str, file: UploadFile = File(...)):
    text = await document_loader.parse_pdf(file)
    chunks = document_loader.chunk_text(text)
    embeddings = openai_client.embed_text(chunks)
    vector_store.add_documents(user_id, chunks, embeddings, sources=[file.filename] * len(chunks))
    return {"message": f"PDF uploaded and indexed for user {user_id}"}

@router.post("/chat", response_model=schemas.ChatResponse)
async def chat(query: str, user_id: str, session_id: str = None):
    """Handle a chat query: retrieve relevant info and get LLM answer."""
    # Retrieve relevant documents from Chroma for this user
    relevant_docs = vector_store.query_documents(user_id, query)
    context = "\n".join([f"Source: {doc['source']}\n{doc['text']}" for doc in relevant_docs])
    # Incorporate conversation history if available
    history = session_manager.get_history(user_id, session_id)
    # Generate answer from OpenAI, with context and history
    answer = openai_client.generate_answer(query, context, history)
    # Save the new question & answer to session history
    session_manager.append_history(user_id, session_id, query, answer)
    print(f"Relevant documents: {relevant_docs}")
    return {"answer": answer, "sources": [{"source": doc["source"], "text": doc["text"]} for doc in relevant_docs]}
