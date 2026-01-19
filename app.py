from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings, invoke_and_save
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_huggingface import ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
from src.db_methods import get_session_history,load_session_history
from src.prompt import *
from src.gemini_script import RotatingGemini
from src.upload_files import UploadResponse
import os
import uuid

#fast api
from __future__ import annotations
import os
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app= FastAPI(title="MedicalChatbot",version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Static and templates
BASE_DIR=Path(__file__).resolve().parent()
static_dir=BASE_DIR/"static"
templates_dir=BASE_DIR/"templates"
app.mount("/static",StaticFiles(directory=str(static_dir)),name="static")
templates=Jinja2Templates(directory=str[templates_dir])

SESSIONS: Dict[str,List[dict]]={}

# ----------------------------
# Adapters
# ----------------------------
class FastAPIFileAdapter:
    """Adapt FastAPI UploadFile to a simple object with .name and .getbuffer()."""
    def __init__(self, uf: UploadFile):
        self._uf = uf
        self.name = uf.filename or "file"

    def getbuffer(self) -> bytes:
        self._uf.file.seek(0)
        return self._uf.file.read()

# Routes
# ----------------------------
@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/upload", response_model=UploadResponse)
async def upload(files: List[UploadFile] = File(...)) -> UploadResponse:
    # if not files:
    #     raise HTTPException(status_code=400, detail="No files uploaded")

    # try:
        # Wrap FastAPI files to preserve filename/ext and provide a read buffer
        wrapped_files = [FastAPIFileAdapter(f) for f in files]

        ingestor = ChatIngestor(use_session_dirs=True)
        session_id = ingestor.session_id

        # Save, load, split, embed, and write FAISS index with MMR
        ingestor.built_retriver(
            uploaded_files=wrapped_files,
            search_type="mmr",
            fetch_k=20,
            lambda_mult=0.5
        )

        # Initialize empty history for this session
        SESSIONS[session_id] = []

        return UploadResponse(session_id=session_id, indexed=True, message="Indexing complete with MMR")
    # except DocumentPortalException as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Upload failed: {e}")


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    session_id = req.session_id
    message = req.message.strip()
    if not session_id or session_id not in SESSIONS:
        raise HTTPException(status_code=400, detail="Invalid or expired session_id. Re-upload documents.")
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        # Build RAG and load retriever from persisted FAISS with MMR
        rag = ConversationalRAG(session_id=session_id)
        index_path = f"faiss_index/{session_id}"
        rag.load_retriever_from_faiss(
            index_path=index_path,
            search_type="mmr",
            fetch_k=20,
            lambda_mult=0.5
        )

        # Use simple in-memory history and convert to BaseMessage list
        simple = SESSIONS.get(session_id, [])
        lc_history = []
        for m in simple:
            role = m.get("role")
            content = m.get("content", "")
            if role == "user":
                lc_history.append(HumanMessage(content=content))
            elif role == "assistant":
                lc_history.append(AIMessage(content=content))

        answer = rag.invoke(message, chat_history=lc_history)

        # Update history
        simple.append({"role": "user", "content": message})
        simple.append({"role": "assistant", "content": answer})
        SESSIONS[session_id] = simple

        return ChatResponse(answer=answer)
    except DocumentPortalException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {e}")



def main():
    print("Hello from chatbotapi")


if __name__=="__main__":
    app.

#initialise flask
# app=Flask(__name__)

load_dotenv()
#load the model
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
keys=[os.getenv("GEMINI_API_KEY_1"),os.getenv("GEMINI_API_KEY_2"),os.getenv("GEMINI_API_KEY_3")]

os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY
keys = [k for k in keys if k]
chatModel = RotatingGemini(api_keys=keys)
embeddings=download_hugging_face_embeddings()

index_name="medical-chatbot"

#Embed each chunk and upsert the embeddings into the Pinecone index.
docsearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever=docsearch.as_retriever(search_type="similarity",search_kwargs={"k":3})

# prompt=ChatPromptTemplate.from_messages(
#     [
#         ("system",system_prompt),
#         ("human","{input}"),
#     ]
# )

# question_answer_chain=create_stuff_documents_chain(chatModel,prompt)
# rag_chain=create_retrieval_chain(retriever,question_answer_chain)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    chatModel, retriever, contextualize_q_prompt
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(chatModel, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

store = {}

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)



@app.route("/")
def index():
    
    # return get_session_history(session_id = 1)
    return render_template('chat.html',get_session_history(session_id = 1))

# @app.route("/get-chats",methods=["GET","POST"])
# def get_chats():
#     print("chats",get_session_history(session_id = 1))
#     return get_session_history(session_id = 1)


@app.route("/get",methods=["GET","POST"])
def chat():
    session_id = request.cookies.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
    msg=request.form["msg"]
    input=msg
    print(input)
    response=invoke_and_save(session_id,msg,conversational_rag_chain)
    print("Response:",response)
    return str(response)


# if __name__=='__main__':
#     app.run()



