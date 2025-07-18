# app/services/document_loader.py
from io import BytesIO
from PyPDF2 import PdfReader
from fastapi import UploadFile

# Max characters per chunk (to fit token limits comfortably, e.g. ~1000 tokens)
CHUNK_SIZE = 2000  

async def parse_pdf(file: UploadFile) -> str:
    try:
        contents = await file.read()
        reader = PdfReader(BytesIO(contents))
        text = "".join(page.extract_text() or "" for page in reader.pages)
        if not text:
            raise ValueError("No text found in the PDF.")
        return text
    except Exception as e:
        raise ValueError(f"Error parsing PDF: {e}")

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    # Simple splitting by chunk_size characters (ensuring we split at sentence boundaries ideally)
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        # Optionally, adjust `end` to nearest sentence end.
        chunks.append(chunk)
        start = end
    return chunks
