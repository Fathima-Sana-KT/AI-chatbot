from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import numpy as np
import logging
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.gpt_integration import huggingface_generate_answer
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# 🔹 Connect to MongoDB
client = MongoClient(settings.MONGO_URI or "mongodb://localhost:27017/")
db = client["ktudb"]
questions_collection = db["questions"]
syllabus_collection = db["syllabus"]

# 🔹 Global variables for TF-IDF indexing
vectorizer = None
tfidf_matrix = None
questions_data = []

# 🔹 Build TF-IDF Index for Existing Questions
def build_tfidf_index():
    global vectorizer, tfidf_matrix, questions_data
    try:
        questions = list(questions_collection.find())
        if not questions:
            logger.warning("No questions found in database for TF-IDF index.")
            vectorizer = None
            tfidf_matrix = None
            questions_data = []
            return

        question_texts = [q["question"].lower() for q in questions]
        questions_data = questions

        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(question_texts)
        logger.info("TF-IDF index built successfully with %d entries.", len(question_texts))
    except Exception as e:
        logger.error(f"Error while building TF-IDF index: {e}")

# Build index at startup
build_tfidf_index()

def get_curriculum_context(scheme: str, branch: str, subject: str) -> str:
    try:
        txt_path = f"data/ktu_btech_{scheme}.txt"
        if not os.path.exists(txt_path):
            return ""
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        content_to_search = content
        if branch:
            branch_map = {
                "CSE": ["COMPUTER SCIENCE AND ENGINEERING", "COMPUTER SCIENCE & ENGINEERING"],
                "ECE": ["ELECTRONICS & COMMUNICATION ENGINEERING", "ELECTRONICS AND COMMUNICATION ENGINEERING"],
                "EEE": ["ELECTRICAL & ELECTRONICS ENGINEERING", "ELECTRICAL AND ELECTRONICS ENGINEERING"],
                "ME": ["MECHANICAL ENGINEERING"],
                "CE": ["CIVIL ENGINEERING"]
            }
            target_headers = branch_map.get(branch.upper(), [])
            start_idx = -1
            for header in target_headers:
                start_idx = content.upper().find(header)
                if start_idx != -1:
                    break
            if start_idx != -1:
                all_possible_next_headers = []
                for b, headers in branch_map.items():
                    if b != branch.upper():
                        for h in headers:
                            idx = content.upper().find(h, start_idx + len(header))
                            if idx != -1:
                                all_possible_next_headers.append(idx)
                end_idx = min(all_possible_next_headers) if all_possible_next_headers else len(content)
                content_to_search = content[start_idx:end_idx]
                
        if subject:
            subject_idx = content_to_search.upper().find(subject.upper())
            if subject_idx != -1:
                content_to_search = content_to_search[subject_idx:subject_idx + 1500]
                
        return content_to_search.strip()
    except Exception as e:
        logger.error(f"Error fetching curriculum context: {e}")
        return ""

# 🔹 Chatbot Response Endpoint with Hybrid Logic
@router.get("/chatbot")
async def get_chatbot_response(query: str, branch: str, subject: str = None, scheme: str = "2019"):
    global vectorizer, tfidf_matrix, questions_data
    try:
        query_cleaned = query.strip().lower()

        # Step 0: Intercept syllabus/course overview requests
        if "explain core topics" in query_cleaned or "syllabus of" in query_cleaned:
            for s in syllabus_collection.find():
                for sub_item in s.get("subjects", []):
                    name = sub_item.get("name", "").lower()
                    code = sub_item.get("code", "").lower()
                    if name in query_cleaned or code in query_cleaned:
                        return {
                            "answer": (
                                f"### 📚 OFFICIAL KTU COURSE OVERVIEW: {sub_item['name']} ({sub_item['code']})\n"
                                f"This is a strictly prescribed APJ Abdul Kalam Technological University (KTU), Kerala "
                                f"B.Tech course for {s['branch']} (Semester {s['semester']}) under the {s['scheme']} Scheme.\n\n"
                                f"The course covers the official syllabus units, thematic structures, and core engineering "
                                f"concepts prescribed by KTU.\n\n"
                                f"### 📊 KTU COURSE EVALUATION METRICS\n"
                                f"- **Continuous Internal Evaluation (CIE):** 50 Marks (Based on 2 internal tests, class assignments, and attendance)\n"
                                f"- **End Semester Examination (ESE):** 100 Marks (3-hour comprehensive written exam)\n"
                                f"- **Total course weightage:** 150 Marks\n\n"
                                f"*(Note: You can use the search curriculum PDF bar below to search specific detailed topics in the PDF files, or select a question paper to view evaluator-approved answers.)*"
                            ),
                            "examples": [],
                            "formulas": [],
                            "source": "DB"
                        }

        # Step 1: Search MongoDB using TF-IDF cosine similarity
        if vectorizer is not None and tfidf_matrix is not None and len(questions_data) > 0:
            query_vector = vectorizer.transform([query_cleaned])
            similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
            best_match_index = np.argmax(similarities)
            best_score = similarities[best_match_index]

            logger.info(f"TF-IDF best match similarity score: {best_score:.4f}")

            # Higher score = more similar (threshold 0.5 is robust for bigram matching)
            if best_score > 0.5:
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

        # Post-process response to construct highly detailed university study format
        detailed_answer = (
            f"### 📝 CONCEPT DEFINITION & OVERVIEW\n"
            f"{gpt_answer}\n\n"
            f"### 📊 KTU EVALUATION MARKING SCHEME BREAKDOWN\n"
            f"For an exam question of this type, KTU evaluators typically award marks based on the following breakdown:\n"
            f"- **Conceptual Definition & Terminology:** 3 Marks (Accurate description and appropriate technical keywords)\n"
            f"- **Technical Features & Architectural Explanation:** 4 Marks (Key points, flowcharts, or structural design)\n"
            f"- **Comparative Analysis / Practical Examples:** 3 Marks (Relevant real-world applications or case studies)\n"
            f"- **Total: 10 Marks**\n\n"
            f"*(Tip: Ensure to draw neat diagrams where applicable, as KTU examiners award up to 30% of the question's total marks for clear illustrations.)*"
        )

        # Step 3: Check AI output before storing
        if gpt_answer and gpt_answer.strip() and len(gpt_answer.strip()) > 10 and "AI generation failed" not in gpt_answer.lower():
            fallback_data = {
                "question": query_cleaned,
                "branch": branch.upper(),
                "answer": detailed_answer,
                "examples": [],
                "formulas": [],
                "source": "AI",
                "verified": False
            }
            try:
                questions_collection.insert_one(fallback_data)
                logger.info("✅ Fallback answer stored in DB.")
                
                # Dynamically update TF-IDF index
                build_tfidf_index()
            except Exception as db_err:
                logger.error(f"❌ Failed to insert fallback answer into DB: {db_err}")
        else:
            logger.warning("⚠️ AI answer not stored due to failure or weak content.")

        return {
            "answer": detailed_answer,
            "examples": [],
            "formulas": [],
            "source": "AI"
        }

    except Exception as e:
        logger.error(f"Chatbot route error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# 🔹 Syllabus Retrieval Endpoint
@router.get("/syllabus")
async def get_syllabus(branch: str, semester: int, scheme: str = "2019"):
    try:
        result = syllabus_collection.find_one({
            "branch": branch.upper(),
            "semester": semester,
            "scheme": scheme
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

# 🔹 Curriculum Search Endpoint (searches parsed PDF curriculum text files)
@router.get("/curriculum-search")
async def search_curriculum_text(query: str, scheme: str = "2019", branch: str = None, subject: str = None):
    try:
        txt_path = f"data/ktu_btech_{scheme}.txt"
        if not os.path.exists(txt_path):
            raise HTTPException(status_code=404, detail=f"Parsed curriculum text not found for scheme {scheme}")
        
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        content_to_search = content
        
        # Filter by branch if specified
        if branch:
            branch_map = {
                "CSE": ["COMPUTER SCIENCE AND ENGINEERING", "COMPUTER SCIENCE & ENGINEERING"],
                "ECE": ["ELECTRONICS & COMMUNICATION ENGINEERING", "ELECTRONICS AND COMMUNICATION ENGINEERING"],
                "EEE": ["ELECTRICAL & ELECTRONICS ENGINEERING", "ELECTRICAL AND ELECTRONICS ENGINEERING"],
                "ME": ["MECHANICAL ENGINEERING"],
                "CE": ["CIVIL ENGINEERING"]
            }
            target_headers = branch_map.get(branch.upper(), [])
            start_idx = -1
            for header in target_headers:
                start_idx = content.upper().find(header)
                if start_idx != -1:
                    break
            
            if start_idx != -1:
                # Find the start of any other branch to stop search slice
                all_possible_next_headers = []
                for b, headers in branch_map.items():
                    if b != branch.upper():
                        for h in headers:
                            idx = content.upper().find(h, start_idx + len(header))
                            if idx != -1:
                                all_possible_next_headers.append(idx)
                
                end_idx = min(all_possible_next_headers) if all_possible_next_headers else len(content)
                content_to_search = content[start_idx:end_idx]
                
        # Filter by subject if specified
        if subject:
            subject_idx = content_to_search.upper().find(subject.upper())
            if subject_idx != -1:
                # Isolate a 4000-character window around the subject's curriculum page block
                content_to_search = content_to_search[subject_idx:subject_idx + 4000]
        
        # Split text into paragraphs
        paragraphs = content_to_search.split("\n\n")
        matches = []
        query_words = query.lower().split()
        
        for para in paragraphs:
            para_clean = para.strip()
            if not para_clean:
                continue
            # Check if any query word is present in paragraph
            if any(word in para_clean.lower() for word in query_words):
                # Clean up multiple spaces/newlines inside paragraphs
                para_clean = " ".join(para_clean.split())
                matches.append(para_clean)
                if len(matches) >= 5: # Limit to top 5 snippets
                    break
        
        return {
            "scheme": scheme,
            "query": query,
            "results": matches if matches else ["No direct matches found in curriculum PDFs."]
        }
    except Exception as e:
        logger.error(f"Curriculum search error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# 🔹 Question Papers Retrieval Endpoint
@router.get("/question-papers")
async def get_question_papers(branch: str, semester: int, scheme: str = "2019", subject: str = None):
    try:
        query_filter = {
            "branch": branch.upper(),
            "semester": semester,
            "scheme": scheme
        }
        if subject:
            query_filter["subject"] = {"$regex": subject, "$options": "i"}
            
        qps_collection = db["question_papers"]
        results = list(qps_collection.find(query_filter))
        
        # Convert ObjectId to string for JSON serialization
        for r in results:
            r["_id"] = str(r["_id"])
            
        return {
            "question_papers": results
        }
    except Exception as e:
        logger.error(f"Question papers route error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


