from app.database import mongo_db

def search_ktu_data(query):
    result = mongo_db["syllabus"].find_one({"topic": query})
    return result["content"] if result else None
