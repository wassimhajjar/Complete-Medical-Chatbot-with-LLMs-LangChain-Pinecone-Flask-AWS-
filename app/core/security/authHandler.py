import jwt
from dotenv import load_dotenv
import time
import os

load_dotenv()

JWT_SECRET=os.getenv("JWT_SECRET")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")

class AuthHandler(object):
    @staticmethod
    def sign_jwt(user_id:int)->str :
        payload={
            "user_id":user_id,
            "expires": time.time() +900
        }
        
        # token=jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
        token=jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
        print("token",token)
        return token
        
    @staticmethod
    def decode_jwt(token:str)->dict:
        print("token2",token)
        try:
            decoded_token=jwt.decode(token,JWT_SECRET,algorithms=JWT_ALGORITHM)
            print("decoded_token",decoded_token)
            return decoded_token if decoded_token["expires"]>=time.time() else None
        except Exception as error:
            print("Unable to decode the token Error\n",error)
            return None