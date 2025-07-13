ktu_syllabus = [
    {
        "branch": "Computer Science",
        "subject": "Data Structures",
        "content": "Linked lists store data in nodes with pointers. Trees are hierarchical structures used in databases and AI.",
        "examples": ["Example: Insertion in a Binary Search Tree (BST)"],
        "formulas": ["Time Complexity of QuickSort: O(n log n)"]
    },
    {
        "branch": "Mechanical",
        "subject": "Thermodynamics",
        "content": "The first law states that energy is conserved in a system.",
        "examples": ["Example: Efficiency calculation of a Carnot Engine"],
        "formulas": ["Work Done in Thermodynamics: W = PΔV"]
    }
]
mongo_db.syllabus.insert_many(ktu_syllabus)
