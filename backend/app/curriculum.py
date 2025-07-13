# backend/app/curriculum.py
def search_curriculum(message: str):
    """
    Searches the curriculum database for subjects or topics based on the user query.
    This function assumes you already have a PostgreSQL or MongoDB database in place.
    """
    # Here you will connect to the database and query for the curriculum data
    # For demonstration, I'm using mock data
    return [
        {"subject_name": "Data Structures", "topic": "Arrays, Linked Lists, Stacks"},
        {"subject_name": "Algorithms", "topic": "Sorting, Searching, Graphs"}
    ]
