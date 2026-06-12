# backend/insert_sample_data.py

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ktudb"]
collection = db["questions"]

sample_data = [
    {
        "question": "How many subjects are there in S3 Maths for CSE?",
        "answer": "There are typically 5 core subjects in S3 for CSE, including Engineering Mathematics.",
        "examples": ["Engineering Mathematics - III", "Discrete Mathematical Structures"],
        "formulas": ["Laplace Transform: L{f(t)} = ∫₀^∞ e^(-st)f(t)dt"]
    },
    {
        "question": "What are the topics in S4 Engineering Mathematics?",
        "answer": "Topics include Complex Analysis, Fourier Series, and PDEs.",
        "examples": ["Complex Numbers", "Fourier Transform"],
        "formulas": ["Euler's Formula: e^(ix) = cos(x) + i*sin(x)"]
    }
]

collection.insert_many(sample_data)
print("Sample data inserted successfully.")
