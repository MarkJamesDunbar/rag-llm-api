FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Create directory for Chroma data
RUN mkdir -p /app/chroma_data
ENV CHROMA_PERSIST_DIR=/app/chroma_data
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
