from .base import BaseRepository
from app.db.models.message import Message
from app.db.schemas.message import MessageInCreate
from typing import List
from app.core.security.authHandler import AuthHandler
from dotenv import load_dotenv
from fastapi import HTTPException 
import datetime
from src.helper import invoke_and_save

load_dotenv()

class MessageRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        
    
    def create_message(self,message_data:MessageInCreate,token,conversational_rag_chain):
        payload=AuthHandler.decode_jwt(token=token)
        print("payload",payload)
        user_id=payload["user_id"]
        newMessage=Message(**message_data.model_dump(exclude_none=True))
        newMessage.timestamps=datetime.datetime.now()
        newMessage.user_id=user_id
        self.session.add(instance=newMessage)
        self.session.commit()
        self.session.refresh(instance=newMessage)
        result = invoke_and_save(user_id,newMessage.content,conversational_rag_chain=conversational_rag_chain)
        aiMessage=MessageInCreate(role="ai",content=result)
        airesponse=Message(**aiMessage.model_dump(exclude_none=True))
        airesponse.timestamps=datetime.datetime.now()
        airesponse.user_id=user_id
        self.session.add(instance=airesponse)
        self.session.commit()
        self.session.refresh(instance=airesponse)
        return airesponse
    
    def get_messages_by_userid(self,user_id,token)->List[Message]:
        payload=AuthHandler.decode_jwt(token=token)
        id=payload["user_id"]
        if user_id==id:
            messages=self.session.query(Message).filter_by(user_id=user_id)
            return messages
        else:
            raise HTTPException(status_code=404,detail="Not found")
            
    
    def get_message_by_id(self,message_id:int)->Message:
        message=self.session.query(Message).filter_by(id=message_id).first()
        return message
    
    def get_messages_by_role(self,role:str)->Message:
        messages=self.session.query(Message).filter_by(role=role)
        return messages