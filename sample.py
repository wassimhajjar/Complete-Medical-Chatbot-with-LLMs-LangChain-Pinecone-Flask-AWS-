from src.rag_methods import get_user_history
import json
user=get_user_history(2)

print("session = ",session.messages)