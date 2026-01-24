from pydantic import EmailStr,BaseModel
from typing import Union

#what to expect to receive from the front-end
class UserInCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

#from the backend to the db
class UserOutput(BaseModel):
   id:int
   name:str
   email:EmailStr

#update user
class UserInUpdate(BaseModel):
   id:int
   name:Union[str,None]=None
   email:Union[EmailStr,None]=None
   password:Union[str,None]=None #or str| None
   
#login user
class UserInLogin(BaseModel):
    email:EmailStr
    password:str
    
#tokens
class UserWithToken(BaseModel):
    token:str