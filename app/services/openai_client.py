# app/services/openai_client.py
import os
from typing import List
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client using the API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define constants for the embedding and chat models
EMBED_MODEL = "text-embedding-ada-002"
CHAT_MODEL = "gpt-3.5-turbo"

def embed_text(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of text chunks using the OpenAI API.
    """
    try:
        # Create embeddings for the input texts
        response = client.embeddings.create(
            model=EMBED_MODEL,
            input=texts
        )
        # Extract the embeddings from the response
        embeddings = [item.embedding for item in response.data]
        return embeddings
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return []

def generate_answer(query: str, context: str, history: List[ChatCompletionMessageParam] = None) -> str:
    """
    Generate an answer to the query using the provided context and chat history.
    """
    # Define the system prompt
    system_prompt = (
        "You are a helpful assistant. Use the provided context to answer the question. "
        "If the context is insufficient, say you don't know."
    )

    # Initialize the messages list with the system prompt
    messages: List[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt}
    ]

    # Add the context as an assistant message if provided
    if context:
        messages.append({"role": "assistant", "content": f"Context:\n{context}"})

    # Extend the messages with the chat history if provided
    if history:
        messages.extend(history)

    # Append the user's query
    messages.append({"role": "user", "content": query})

    try:
        # Create a chat completion using the OpenAI API
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages
        )
        # Return the assistant's reply
        return response.choices[0].message.content
    except Exception as e:
        print(f"Exception occurred: {e}")
        return "An error occurred while generating the answer."
