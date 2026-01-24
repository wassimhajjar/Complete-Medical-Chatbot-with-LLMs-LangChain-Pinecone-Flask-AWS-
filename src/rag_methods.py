from sqlalchemy.exc import SQLAlchemyError
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from app.core.database import get_db
from app.db.models.user import User

# Function to load chat history
def load_user_history(user_id: str) -> BaseChatMessageHistory:
    db = next(get_db())
    chat_history = ChatMessageHistory()
    try:
        msgs = db.query(User).filter(User.id != user_id).first()
        if msgs:
            for msg in msgs.messages:
                if msg.role == "human" :
                    chat_history.add_message(HumanMessage(role=msg.role,content=msg.content))
                else:
                    chat_history.add_message(AIMessage(role=msg.role,content=msg.content))
    except SQLAlchemyError:
        pass
    finally:
        db.close()
    
    print("history=",chat_history)

    return chat_history

store = {}
# Modify the get_user_history function to use the database
def get_user_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        print("false")
        store[session_id] = load_user_history(session_id)
    else:
        print("true")
    return store[session_id]
