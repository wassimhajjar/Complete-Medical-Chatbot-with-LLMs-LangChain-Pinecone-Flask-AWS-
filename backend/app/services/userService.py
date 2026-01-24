from app.db.repository.userRepository import UserRepository
from app.db.schemas.user import UserOutput,UserInCreate,UserInLogin,UserWithToken
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException

class UserService:
    def __init__(self,session:Session):
        self.__userRepository=UserRepository(session=session)
    
    def signup(self,user_details:UserInCreate)->UserOutput:
        if self.__userRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=400,detail="Registered account. Please login")
        hashed_password=HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password=hashed_password
        return self.__userRepository.create_user(user_data=user_details)
    
    def login(self,login_details:UserInLogin)->UserWithToken:
        if not self.__userRepository.get_user_by_email(email=login_details.email):
            raise HTTPException(status_code=400, detail="Please create an Account")
        
        user=self.__userRepository.get_user_by_email(email=login_details.email)
        if HashHelper.verify_password(plain_password=login_details.password,hashed_password=user.password):
            token=AuthHandler.sign_jwt(user_id=user.id)
            print("token login",UserWithToken(token=token))
            if token:
                return UserWithToken(token=token)
            else:
                raise HTTPException(status_code=400,detail="Unable to process request")
        raise HTTPException(status_code=400,detail="Please check your Credentials")
    
    def get_user_by_id(self,user_id:int): 
        user=self.__userRepository.get_user_by_id(user_id=user_id)
        if user:
            return user
        else:
            raise HTTPException(status_code=400,detail="User is not available")   
        