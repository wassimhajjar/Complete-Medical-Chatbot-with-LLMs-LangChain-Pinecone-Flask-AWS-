from src.db_methods import get_session_history
import json
session=get_session_history(2)

print("session = ",session.messages)