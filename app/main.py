# filepath: /Users/markdunbar/Documents/Repositories/rag-llm-api/app/main.py
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI()

app.include_router(router)