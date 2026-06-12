from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ktudb"]
syllabus_collection = db["syllabus"]

# Clear existing
syllabus_collection.delete_many({})

ktu_syllabus = [
    {
        "branch": "CSE",
        "semester": 3,
        "subjects": [
            {"name": "Discrete Mathematical Structures", "code": "MAT203"},
            {"name": "Data Structures", "code": "CST201"},
            {"name": "Computer Organization and Architecture", "code": "CST203"},
            {"name": "Object Oriented Programming using Java", "code": "CST205"},
            {"name": "Sustainable Engineering", "code": "MCN201"}
        ]
    },
    {
        "branch": "CSE",
        "semester": 4,
        "subjects": [
            {"name": "Probability, Random Processes and Numerical Methods", "code": "MAT204"},
            {"name": "Database Management Systems", "code": "CST202"},
            {"name": "Operating Systems", "code": "CST204"},
            {"name": "Design and Analysis of Algorithms", "code": "CST206"},
            {"name": "Constitution of India", "code": "MCN202"}
        ]
    },
    {
        "branch": "ECE",
        "semester": 3,
        "subjects": [
            {"name": "Partial Differential Equations and Complex Analysis", "code": "MAT201"},
            {"name": "Solid State Devices", "code": "ECT201"},
            {"name": "Network Theory", "code": "ECT203"},
            {"name": "Logic Circuit Design", "code": "ECT205"},
            {"name": "Sustainable Engineering", "code": "MCN201"}
        ]
    }
]

syllabus_collection.insert_many(ktu_syllabus)
print("Syllabus seeded successfully.")
