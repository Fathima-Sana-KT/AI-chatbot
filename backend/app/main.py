from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import chatbot  # Chatbot route file
from app.utils.pdf_parser import save_curriculum_to_txt  # PDF parsing utility
from app.auth import auth  # Auth router module
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AcadeMate API",
    version="1.0",
    description="Backend for AcadeMate - KTU Student Support Chatbot"
)

#  Include Auth Router
app.include_router(auth.auth_router, prefix="/auth", tags=["Auth API"])

#  CORS Middleware - allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  On startup: Parse curriculum PDFs if not already parsed
@app.on_event("startup")
async def parse_curriculum_on_startup():
    curriculum_files = [
        ("data/ktu_pdfs/ktu_curriculum_2019.pdf", "data/ktu_btech_2019.txt"),
        ("data/ktu_pdfs/ktu_curriculum_2024.pdf", "data/ktu_btech_2024.txt"),
    ]

    for pdf_path, txt_path in curriculum_files:
        if not os.path.exists(txt_path):
            logger.info(f"Parsing curriculum PDF: {pdf_path}")
            save_curriculum_to_txt(pdf_path, txt_path)
        else:
            logger.info(f"Curriculum already parsed: {txt_path}")

# Health check route
@app.get("/")
async def root():
    return {"message": "AcadeMate backend is running successfully!"}

# Include Chatbot Routes
app.include_router(chatbot.router, prefix="/chat", tags=["Chatbot API"])








