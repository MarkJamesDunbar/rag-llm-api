# app/services/session_manager.py
from collections import defaultdict

# In-memory storage: { (user_id, session_id): [message_dict, ...] }
user_sessions = defaultdict(list)

def get_history(user_id: str, session_id: str = None) -> list[dict]:
    """Retrieve the chat history for a given user (and session)."""
    key = (user_id, session_id or user_id)
    return user_sessions.get(key, []).copy()

def append_history(user_id: str, session_id: str, user_query: str, assistant_answer: str):
    """Append the latest user query and assistant answer to the history."""
    key = (user_id, session_id or user_id)
    convo = user_sessions.get(key, [])
    convo.append({"role": "user", "content": user_query})
    convo.append({"role": "assistant", "content": assistant_answer})
    user_sessions[key] = convo