from pydantic import BaseModel,Field
from typing import Annotated
from enum import Enum

class UploadResponse(BaseModel):
    session_id:str
    indexed:bool
    message:str | None = None

class ChatRequest(BaseModel):
    session_id:str
    message:str

class ChatResponse(BaseModel):
    answer:str