from __future__ import annotations
from src.helper import  invoke_and_save
from src.prompt import *
from src.helper import initialize
from src.rag_methods import get_session_history
import os
from pathlib import Path
from typing import Dict
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
# from app.db. import Message
from app.router.auth import authRouter
from app.router.message import messageRouter
from app.util.protectRoute import get_current_user
from app.db.schemas.user import UserOutput
from contextlib import asynccontextmanager
from app.util.db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

# fast api
app= FastAPI(title="MedicalChatbot",version="0.1.0",lifespan=lifespan)
app.include_router(router=authRouter,tags=["auth"])
app.include_router(dependencies=[Depends(get_current_user)],router=messageRouter,tags=["message"])
conversational_rag_chain = initialize()

origins = [
    "http://localhost:5173",  # Default Vite React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)


# Static and templates
BASE_DIR=Path(__file__).resolve().parent
static_dir=BASE_DIR/"static"
templates_dir=BASE_DIR/"templates"
app.mount("/static",StaticFiles(directory=str(static_dir)),name="static")
templates=Jinja2Templates(directory=str(templates_dir))



# Routes
# ----------------------------

@app.get("/health")
def health_check():
    return {"status":"Running..."}

@app.get("/protected")
def read_protected(user:UserOutput=Depends(get_current_user)):
    return user

# @app.get("/health")
# def health() -> Dict[str, str]:
#     return {"status": "ok"}


# @app.get("/", response_class=HTMLResponse)
# def home(request: Request) -> HTMLResponse:
#     return templates.TemplateResponse("index.html", {"request": request})
    

# @app.get("/get-session")
# def get_session():
#     return get_session_history(1)

# @app.post("/chat")
# async def add_chats(chat:Message,request:Request):
#     session_id = request.cookies.get('chat_session_id')
#     if not session_id:
#         session_id = str(uuid.uuid4())
#     data=await request.json()
#     msg=data.get("content")
#     session_id=data.get("session_id")
#     input=msg
#     print("data",data)
#     response=invoke_and_save(session_id,msg,conversational_rag_chain)
#     print("Response:",response)
#     return str(response)

# # Uvicorn entrypoint for `python main.py` (optional)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=int(os.getenv("PORT", "8001")),reload=True)


    
    
