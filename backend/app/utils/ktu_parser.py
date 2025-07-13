def search_syllabus(query, branch=None):
    """
    Searches the KTU syllabus in MongoDB based on the user's query.
    :param query: User's input/question
    :param branch: (Optional) Engineering branch to filter results
    :return: Relevant syllabus content or an error message
    """
    search_filter = {}
    if branch:
        search_filter["branch"] = branch
    
    # Fetch syllabus data from MongoDB
    from app.database import mongo_db
    results = list(mongo_db.syllabus.find({"topic": {"$regex": query, "$options": "i"}}))




    if not results:
        return {"content": "Sorry, no information available.", "examples": [], "formulas": []}

    # Return first matching result
    return results[0]
