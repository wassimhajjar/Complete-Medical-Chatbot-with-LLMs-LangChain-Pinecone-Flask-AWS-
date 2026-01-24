from fastapi import APIRouter,Depends
from app.core.database import get_db
from app.services.messageService import MessageService
from app.db.schemas.message import MessageInCreate,MessageOutput
from typing import List
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from main import conversational_rag_chain

messageRouter=APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# oauth2_scheme = OAuth2AuthorizationCodeBearer(  
#     tokenUrl="http://keycloak.kube/realms/juju/protocol/openid-connect/token",  
#     authorizationUrl="http://keycloak.kube/realms/juju/protocol/openid-connect/auth",  
#     refreshUrl="http://keycloak.kube/realms/juju/protocol/openid-connect/token",
#     scopes={"openid": "description"}  
# )

@messageRouter.post("/messages",status_code=200,response_model=MessageOutput)
def add(messageDetails:MessageInCreate,session: Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    return MessageService(session=session).add(message_details=messageDetails,token=token,conversational_rag_chain=conversational_rag_chain)

@messageRouter.get("/messages/{user_id}",status_code=200,response_model=List[MessageOutput])
def get(user_id: int,session:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    return MessageService(session=session).get(user_id=user_id,token=token)