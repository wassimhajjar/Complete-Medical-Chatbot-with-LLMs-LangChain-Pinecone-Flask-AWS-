from app.core.database import Base
from sqlalchemy import Column, Integer,String,ForeignKey,Text
from sqlalchemy.orm import relationship


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user = relationship("User", back_populates="messages")
    timestamps= Column(String,nullable=False)
