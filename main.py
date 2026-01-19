from __future__ import annotations
from flask import Flask, render_template, request
from src.helper import  invoke_and_save
from src.prompt import *
from src.helper import initialize
import uuid
from src.db_methods import get_session_history
import os
from pathlib import Path
from typing import Dict, List
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from src.models.message import Message

# fast api
app= FastAPI(title="MedicalChatbot",version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and templates
BASE_DIR=Path(__file__).resolve().parent
static_dir=BASE_DIR/"static"
templates_dir=BASE_DIR/"templates"
app.mount("/static",StaticFiles(directory=str(static_dir)),name="static")
templates=Jinja2Templates(directory=str(templates_dir))

conversational_rag_chain = initialize()

# Routes
# ----------------------------
@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})
    

@app.get("/get-session")
def get_session():
    return get_session_history(1)

@app.post("/chat")
async def add_chats(chat:Message,request:Request):
    session_id = request.cookies.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
    data=await request.json()
    msg=data.get("content")
    session_id=data.get("session_id")
    input=msg
    print("data",data)
    response=invoke_and_save(session_id,msg,conversational_rag_chain)
    print("Response:",response)
    return str(response)

# Uvicorn entrypoint for `python main.py` (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=int(os.getenv("PORT", "8001")),reload=True)

