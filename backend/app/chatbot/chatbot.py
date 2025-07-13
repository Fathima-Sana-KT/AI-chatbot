from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import logging

from app.utils.gpt_integration import huggingface_generate_answer
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# 🔹 Connect to MongoDB
client = MongoClient(settings.MONGO_URI or "mongodb://localhost:27017/")
db = client["ktudb"]
questions_collection = db["questions"]
syllabus_collection = db["syllabus"]

# 🔹 Initialize Sentence-BERT Model and FAISS Index
model = SentenceTransformer('all-MiniLM-L6-v2')

# 🔹 Build FAISS Index for Existing Questions
def build_faiss_index():
    try:
        questions = list(questions_collection.find())
        if not questions:
            logger.warning("No questions found in database for FAISS index.")
            return None, []

        question_texts = [q["question"] for q in questions]
        question_embeddings = model.encode(question_texts)
        question_embeddings = np.array(question_embeddings)

        index = faiss.IndexFlatL2(question_embeddings.shape[1])
        index.add(question_embeddings)

        logger.info("FAISS index built successfully with %d entries.", len(question_texts))
        return index, questions

    except Exception as e:
        logger.error(f"Error while building FAISS index: {e}")
        return None, []

# Build index at startup
index, questions_data = build_faiss_index()

# 🔹 Chatbot Response Endpoint with Hybrid Logic
@router.get("/chatbot")
async def get_chatbot_response(query: str, branch: str):
    try:
        query_cleaned = query.strip().lower()

        # Step 1: Search MongoDB using FAISS
        if index and questions_data:
            query_embedding = model.encode([query_cleaned])
            D, I = index.search(np.array(query_embedding), k=1)
            best_match_index = I[0][0]
            similarity_score = D[0][0]

            logger.info(f"FAISS distance score: {similarity_score:.4f}")

            # Lower score = more similar (tweak threshold as needed)
            if similarity_score < 0.6:
                matched_question = questions_data[best_match_index]
                return {
                    "answer": matched_question.get("answer", "No answer found."),
                    "examples": matched_question.get("examples", []),
                    "formulas": matched_question.get("formulas", []),
                    "source": "DB"
                }

        # Step 2: No match found — Fallback to HuggingFace
        logger.info("No DB match found. Generating answer via HuggingFace...")
        gpt_answer = huggingface_generate_answer(query_cleaned)
        logger.debug(f"Raw HuggingFace model output: {gpt_answer}")

        # Step 3: Check AI output before storing
        if gpt_answer and gpt_answer.strip() and len(gpt_answer.strip()) > 10 and "AI generation failed" not in gpt_answer.lower():
            fallback_data = {
                "question": query_cleaned,
                "branch": branch.upper(),
                "answer": gpt_answer,
                "examples": [],
                "formulas": [],
                "source": "AI",
                "verified": False
            }
            try:
                questions_collection.insert_one(fallback_data)
                logger.info("✅ Fallback answer stored in DB.")
            except Exception as db_err:
                logger.error(f"❌ Failed to insert fallback answer into DB: {db_err}")
        else:
            logger.warning("⚠️ AI answer not stored due to failure or weak content.")

        return {
            "answer": gpt_answer,
            "examples": [],
            "formulas": [],
            "source": "AI"
        }

    except Exception as e:
        logger.error(f"Chatbot route error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# 🔹 Syllabus Retrieval Endpoint
@router.get("/syllabus")
async def get_syllabus(branch: str, semester: int):
    try:
        result = syllabus_collection.find_one({
            "branch": branch.upper(),
            "semester": semester
        })

        if result:
            return {
                "subjects": result.get("subjects", [])
            }

        return JSONResponse(status_code=404, content={
            "subjects": [],
            "message": "Syllabus not found."
        })

    except Exception as e:
        logger.error(f"Syllabus route error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

