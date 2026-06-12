from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ktudb"]
qps_collection = db["question_papers"]

# Clear existing
qps_collection.delete_many({})

sample_qps = [
    {
        "branch": "CSE",
        "semester": 3,
        "subject": "Data Structures",
        "year": 2023,
        "exam_type": "Regular",
        "pdf_url": "https://example.com/qps/cse_ds_2023.pdf",
        "questions": [
            "What is a circular linked list? Explain its advantages and disadvantages.",
            "Write the algorithm for Heap Sort and trace it on [15, 5, 20, 1, 10, 8].",
            "Explain AVL tree rotations with suitable diagrams."
        ]
    },
    {
        "branch": "CSE",
        "semester": 3,
        "subject": "Discrete Mathematical Structures",
        "year": 2022,
        "exam_type": "Regular",
        "pdf_url": "https://example.com/qps/cse_dms_2022.pdf",
        "questions": [
            "State and prove Pigeonhole Principle.",
            "Find the transitive closure of the relation R = {(1,2), (2,3), (3,4)} using Warshall's Algorithm.",
            "Show that the set of all subsets of a set forms a Boolean algebra."
        ]
    },
    {
        "branch": "CSE",
        "semester": 4,
        "subject": "Operating Systems",
        "year": 2023,
        "exam_type": "Regular",
        "pdf_url": "https://example.com/qps/cse_os_2023.pdf",
        "questions": [
            "Explain the different CPU scheduling algorithms with examples.",
            "What is deadlock? Explain the Banker's algorithm for deadlock avoidance.",
            "Discuss the differences between paging and segmentation."
        ]
    },
    {
        "branch": "ECE",
        "semester": 3,
        "subject": "Logic Circuit Design",
        "year": 2023,
        "exam_type": "Regular",
        "pdf_url": "https://example.com/qps/ece_lcd_2023.pdf",
        "questions": [
            "Design a 4-bit binary adder-subtractor circuit.",
            "Minimize the boolean function using K-Map: F(A,B,C,D) = Σ(0, 2, 5, 7, 8, 10, 13, 15).",
            "Differentiate between synchronous and asynchronous counters."
        ]
    }
]

qps_collection.insert_many(sample_qps)
print("Question Papers seeded successfully.")
