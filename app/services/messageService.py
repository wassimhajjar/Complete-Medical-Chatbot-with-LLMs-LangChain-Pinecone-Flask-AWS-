from app.db.repository.messageRepository import MessageRepository
from app.db.schemas.message import MessageInCreate,MessageOutput
from sqlalchemy.orm import Session
from typing import List


class MessageService:
    def __init__(self,session:Session):
        self.__messageRepository=MessageRepository(session=session)
    
    def add(self,message_details:MessageInCreate,token,conversational_rag_chain)->MessageOutput:
        return self.__messageRepository.create_message(message_data=message_details,token=token)
    
    def get(self,user_id,token)->List[MessageOutput]:
        return self.__messageRepository.get_messages_by_userid(user_id=user_id,token=token)
    
        
        