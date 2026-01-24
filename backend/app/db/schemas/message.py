from pydantic import BaseModel,constr
from typing import Literal,Annotated

#what to expect to receive from the front-end
class MessageInCreate(BaseModel):
    role:Literal['ai','human']
    content: Annotated[str, 'message content must have at least 1 character']



#from the backend to the db
class MessageOutput(BaseModel):
   id:int
   user_id:int
   role:str
   content:str
   timestamps:str