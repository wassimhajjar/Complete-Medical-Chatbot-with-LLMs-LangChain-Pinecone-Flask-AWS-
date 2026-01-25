from __future__ import annotations
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.router.auth import authRouter
from app.router.message import messageRouter
from app.util.protectRoute import get_current_user
from contextlib import asynccontextmanager
from app.util.db import create_tables
from dotenv import load_dotenv
import os

load_dotenv()

front_end_url=os.getenv("FRONT_END_URL")
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

# fast api
app= FastAPI(title="MedicalChatbot",version="0.1.0",lifespan=lifespan)
app.include_router(router=authRouter,tags=["auth"])
app.include_router(dependencies=[Depends(get_current_user)],router=messageRouter,tags=["message"])

#development only
# origins = [
#     front_end_url,
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)