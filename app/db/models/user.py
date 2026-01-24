from app.core.database import Base
from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String(200))
    email=Column(String(100),unique=True)
    password=Column(String(250))
    messages = relationship("Message", back_populates="user")


    