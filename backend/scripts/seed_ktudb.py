from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ktudb"]

# Collections
syllabus_collection = db["syllabus"]
qps_collection = db["question_papers"]
questions_collection = db["questions"]

# Clear existing entries
syllabus_collection.delete_many({})
qps_collection.delete_many({})
questions_collection.delete_many({"source": {"$ne": "USER"}})

print("Cleared existing DB entries for seeding strict KTU syllabus.")

branches = ["CSE", "ECE", "EEE", "ME", "CE"]
semesters = [1, 2, 3, 4, 5, 6, 7, 8]
schemes = ["2019", "2024"]

# Strictly KTU B.Tech 2019 Scheme subjects
subjects_2019 = {
    "CSE": {
        1: [
            ("Linear Algebra and Calculus", "MAT101"),
            ("Engineering Physics A", "PHT100"),
            ("Engineering Mechanics", "EST100"),
            ("Basics of Civil & Mechanical Engineering", "EST120"),
            ("Life Skills", "HUN101"),
            ("Engineering Physics Lab", "PHL120"),
            ("Civil & Mechanical Workshop", "ESL120")
        ],
        2: [
            ("Vector Calculus, Differential Equations and Transforms", "MAT102"),
            ("Engineering Chemistry", "CYT100"),
            ("Engineering Graphics", "EST110"),
            ("Basics of Electrical & Electronics Engineering", "EST130"),
            ("Professional Communication", "HUN102"),
            ("Programming in C", "EST102"),
            ("Engineering Chemistry Lab", "CYL120"),
            ("Electrical & Electronics Workshop", "ESL130")
        ],
        3: [
            ("Discrete Mathematical Structures", "MAT203"),
            ("Data Structures", "CST201"),
            ("Logic System Design", "CST203"),
            ("Object Oriented Programming using Java", "CST205"),
            ("Design & Engineering", "EST200"),
            ("Sustainable Engineering", "MCN201"),
            ("Data Structures Lab", "CSL201"),
            ("Object Oriented Programming Lab (in Java)", "CSL203")
        ],
        4: [
            ("Graph Theory", "MAT206"),
            ("Computer Organisation and Architecture", "CST202"),
            ("Database Management Systems", "CST204"),
            ("Operating Systems", "CST206"),
            ("Design and Analysis of Algorithms", "CST208"),
            ("Constitution of India", "MCN202"),
            ("Digital Lab", "CSL202"),
            ("Operating Systems Lab", "CSL204")
        ],
        5: [
            ("Formal Languages and Automata Theory", "CST301"),
            ("Computer Networks", "CST303"),
            ("System Software", "CST305"),
            ("Microprocessors and Microcontrollers", "CST307"),
            ("Disaster Management", "MCN301"),
            ("System Software and Microprocessors Lab", "CSL331"),
            ("Database Management Systems Lab", "CSL333")
        ],
        6: [
            ("Compiler Design", "CST302"),
            ("Computer Graphics and Image Processing", "CST304"),
            ("Software Engineering and Project Management", "CST306"),
            ("Comprehensive Course Work", "CST308"),
            ("Microcontrollers Lab", "CSL332"),
            ("Miniproject", "CSL334")
        ],
        7: [
            ("Artificial Intelligence", "CST401"),
            ("Distributed Computing", "CST403"),
            ("Industrial Safety Engineering", "MCN401"),
            ("Compiler Lab", "CSL411"),
            ("Seminar", "CSQ413"),
            ("Project Phase I", "CSD415")
        ],
        8: [
            ("Distributed Computing", "CST402"),
            ("Soft Computing", "CST444"),
            ("Data Mining", "CST466"),
            ("Software Testing", "CST458"),
            ("Security in Computing", "CST404"),
            ("Project Phase II", "CSD416")
        ]
    },
    "ECE": {
        1: [
            ("Linear Algebra and Calculus", "MAT101"),
            ("Engineering Physics A", "PHT100"),
            ("Engineering Mechanics", "EST100"),
            ("Basics of Civil & Mechanical Engineering", "EST120"),
            ("Life Skills", "HUN101")
        ],
        2: [
            ("Vector Calculus, Differential Equations and Transforms", "MAT102"),
            ("Engineering Chemistry", "CYT100"),
            ("Engineering Graphics", "EST110"),
            ("Basics of Electrical & Electronics Engineering", "EST130"),
            ("Professional Communication", "HUN102"),
            ("Programming in C", "EST102")
        ],
        3: [
            ("Partial Differential Equations and Complex Analysis", "MAT201"),
            ("Solid State Devices", "ECT201"),
            ("Network Theory", "ECT203"),
            ("Logic Circuit Design", "ECT205"),
            ("Design & Engineering", "EST200"),
            ("Sustainable Engineering", "MCN201"),
            ("Scientific Computing Lab", "ECL201"),
            ("Logic Design Lab", "ECL203")
        ],
        4: [
            ("Probability, Random Processes and Numerical Methods", "MAT204"),
            ("Analog Circuits", "ECT202"),
            ("Signals and Systems", "ECT204"),
            ("Computer Architecture", "ECT206"),
            ("Professional Ethics", "HUT200"),
            ("Constitution of India", "MCN202"),
            ("Analog Circuits and Simulation Lab", "ECL202"),
            ("Microcontrollers Lab", "ECL204")
        ],
        5: [
            ("Digital Communication", "ECT301"),
            ("Linear Integrated Circuits", "ECT303"),
            ("Microcontrollers", "ECT305"),
            ("Electromagnetic Waves", "ECT307"),
            ("Disaster Management", "MCN301")
        ],
        6: [
            ("Digital Signal Processing", "ECT302"),
            ("VLSI Design", "ECT304"),
            ("Information Theory and Coding", "ECT306"),
            ("Comprehensive Course Work", "ECT308")
        ],
        7: [
            ("Microwave and Radar Engineering", "ECT401"),
            ("Optical Communication", "ECT403"),
            ("Industrial Safety Engineering", "MCN401")
        ],
        8: [
            ("Wireless Communication", "ECT402"),
            ("Advanced Communication Systems", "ECT404")
        ]
    },
    "EEE": {
        1: [
            ("Linear Algebra and Calculus", "MAT101"),
            ("Engineering Physics A", "PHT100"),
            ("Engineering Mechanics", "EST100"),
            ("Basics of Civil & Mechanical Engineering", "EST120")
        ],
        2: [
            ("Vector Calculus, Differential Equations and Transforms", "MAT102"),
            ("Engineering Chemistry", "CYT100"),
            ("Engineering Graphics", "EST110"),
            ("Basics of Electrical & Electronics Engineering", "EST130"),
            ("Programming in C", "EST102")
        ],
        3: [
            ("Partial Differential Equations and Complex Analysis", "MAT201"),
            ("Circuits and Networks", "EET201"),
            ("Analog Electronics", "EET203"),
            ("DC Machines and Transformers", "EET205"),
            ("Design & Engineering", "EST200"),
            ("Sustainable Engineering", "MCN201")
        ],
        4: [
            ("Mathematics IV (Complex Variables and Physical Sciences)", "MAT202"),
            ("Digital Electronics", "EET202"),
            ("Power Systems I", "EET204"),
            ("AC Machines", "EET206"),
            ("Professional Ethics", "HUT200"),
            ("Constitution of India", "MCN202")
        ],
        5: [
            ("Power Electronics", "EET301"),
            ("Control Systems", "EET303"),
            ("Microprocessors and Embedded Systems", "EET305"),
            ("Signals and Systems", "EET307")
        ],
        6: [
            ("Power Systems II", "EET302"),
            ("Advanced Control Systems", "EET304"),
            ("Power System Analysis", "EET306")
        ],
        7: [
            ("Electrical System Design", "EET401"),
            ("Power System Protection", "EET403")
        ],
        8: [
            ("Industrial Instrumentation", "EET402"),
            ("Smart Grid Technologies", "EET404")
        ]
    },
    "ME": {
        1: [
            ("Linear Algebra and Calculus", "MAT101"),
            ("Engineering Physics B", "PHT110"),
            ("Engineering Mechanics", "EST100"),
            ("Basics of Electrical & Electronics Engineering", "EST130")
        ],
        2: [
            ("Vector Calculus, Differential Equations and Transforms", "MAT102"),
            ("Engineering Chemistry", "CYT100"),
            ("Engineering Graphics", "EST110"),
            ("Basics of Civil & Mechanical Engineering", "EST120"),
            ("Programming in C", "EST102")
        ],
        3: [
            ("Partial Differential Equations and Complex Analysis", "MAT201"),
            ("Mechanics of Solids", "MET201"),
            ("Mechanics of Fluids", "MET203"),
            ("Metallurgy and Material Science", "MET205"),
            ("Design & Engineering", "EST200"),
            ("Sustainable Engineering", "MCN201")
        ],
        4: [
            ("Engineering Mathematics IV", "MAT202"),
            ("Thermodynamics", "MET202"),
            ("Manufacturing Technology", "MET204"),
            ("Fluid Machinery", "MET206"),
            ("Professional Ethics", "HUT200"),
            ("Constitution of India", "MCN202")
        ],
        5: [
            ("Heat and Mass Transfer", "MET301"),
            ("Dynamics of Machinery", "MET303"),
            ("Design of Machine Elements I", "MET305")
        ],
        6: [
            ("Advanced Manufacturing Technology", "MET302"),
            ("Thermal Engineering", "MET304"),
            ("Design of Machine Elements II", "MET306")
        ],
        7: [
            ("Mechatronics", "MET401"),
            ("Energy Engineering", "MET403")
        ],
        8: [
            ("Industrial Engineering", "MET402"),
            ("Computer Integrated Manufacturing", "MET404")
        ]
    },
    "CE": {
        1: [
            ("Linear Algebra and Calculus", "MAT101"),
            ("Engineering Physics B", "PHT110"),
            ("Engineering Mechanics", "EST100"),
            ("Basics of Electrical & Electronics Engineering", "EST130")
        ],
        2: [
            ("Vector Calculus, Differential Equations and Transforms", "MAT102"),
            ("Engineering Chemistry", "CYT100"),
            ("Engineering Graphics", "EST110"),
            ("Basics of Civil & Mechanical Engineering", "EST120"),
            ("Programming in C", "EST102")
        ],
        3: [
            ("Partial Differential Equations and Complex Analysis", "MAT201"),
            ("Mechanics of Solids", "CET201"),
            ("Fluid Mechanics & Hydraulics", "CET203"),
            ("Surveying & Geomatics", "CET205"),
            ("Design & Engineering", "EST200"),
            ("Sustainable Engineering", "MCN201")
        ],
        4: [
            ("Probability, Statistics and Numerical Methods", "MAT202"),
            ("Engineering Geology", "CET202"),
            ("Geotechnical Engineering I", "CET204"),
            ("Transportation Engineering", "CET206"),
            ("Professional Ethics", "HUT200"),
            ("Constitution of India", "MCN202")
        ],
        5: [
            ("Structural Analysis II", "CET301"),
            ("Geotechnical Engineering II", "CET303"),
            ("Design of Concrete Structures I", "CET305")
        ],
        6: [
            ("Design of Steel Structures", "CET302"),
            ("Transportation Engineering II", "CET304"),
            ("Water Resources Engineering", "CET306")
        ],
        7: [
            ("Design of Concrete Structures II", "CET401"),
            ("Environmental Engineering I", "CET403")
        ],
        8: [
            ("Environmental Engineering II", "CET402"),
            ("Construction Management", "CET404")
        ]
    }
}

# Strictly KTU B.Tech 2024 Scheme subjects (modular group-wise)
subjects_2024 = {
    "CSE": {
        1: [
            ("Group Specific Mathematics - I", "GYMAT101"),
            ("Physics for Engineers", "GYPHT121"),
            ("Engineering Graphics and Computer Aided Drawing", "GYEST103"),
            ("Introduction to Electrical & Electronics Engineering", "GYEST104"),
            ("Algorithmic Thinking with Python", "UCEST105"),
            ("Basic Electrical and Electronics Engineering Workshop", "GYESL106"),
            ("Health and Safety", "UCPST127")
        ],
        2: [
            ("Group Specific Mathematics - II", "GYMAT201"),
            ("Chemistry for Engineers", "GYCYT122"),
            ("Foundations of Computing: From Hardware Essentials to Web Design", "GYEST203"),
            ("Programming in C", "GYEST204"),
            ("Life Skills and Universal Human Values", "UCHUT128"),
            ("Digital 101 (NASSCOM)", "UCSEM129")
        ],
        3: [
            ("Discrete Mathematical Structures", "CST201"),
            ("Data Structures & Algorithms", "CST203"),
            ("Digital Logic & System Design", "CST205"),
            ("Object Oriented Programming (Python/Java)", "CST207")
        ],
        4: [
            ("Database Management Systems", "CST202"),
            ("Operating Systems", "CST204"),
            ("Computer Organization and Architecture", "CST206"),
            ("Theory of Computation", "CST208")
        ],
        5: [
            ("Software Engineering & Agile Methodologies", "CST301"),
            ("Computer Networks", "CST303"),
            ("Design and Analysis of Algorithms", "CST305")
        ],
        6: [
            ("Compiler Construction", "CST302"),
            ("Artificial Intelligence & Machine Learning", "CST304"),
            ("Cloud Computing & DevOps", "CST306")
        ],
        7: [
            ("Cryptography and Network Security", "CST401"),
            ("Big Data Analytics & IoT", "CST403")
        ],
        8: [
            ("Distributed Computing", "CST402"),
            ("Soft Computing", "CST444"),
            ("Data Mining", "CST466"),
            ("Software Testing", "CST458"),
            ("Full Stack Web Development", "CST402"),
            ("Comprehensive Project Phase II", "CSD416")
        ]
    },
    "ECE": {
        1: [
            ("Group Specific Mathematics - I", "GYMAT101"),
            ("Physics for Engineers", "GYPHT121"),
            ("Engineering Graphics and Computer Aided Drawing", "GYEST103"),
            ("Introduction to Electrical & Electronics Engineering", "GYEST104"),
            ("Algorithmic Thinking with Python", "UCEST105")
        ],
        2: [
            ("Group Specific Mathematics - II", "GYMAT201"),
            ("Chemistry for Engineers", "GYCYT122"),
            ("Electronic Devices and Circuits", "GYEST203"),
            ("Programming in C", "GYEST204")
        ],
        3: [
            ("Signals and Systems", "ECT201"),
            ("Digital System Design", "ECT203"),
            ("Network Analysis & Synthesis", "ECT205")
        ],
        4: [
            ("Analog Circuits", "ECT202"),
            ("Microcontrollers & Interfacing", "ECT204"),
            ("Electromagnetic Theory", "ECT206")
        ],
        5: [
            ("Digital Signal Processing", "ECT301"),
            ("Analog and Digital Communication", "ECT303")
        ],
        6: [
            ("VLSI Design", "ECT302"),
            ("Antennas and Wave Propagation", "ECT304")
        ],
        7: [
            ("Microwave Engineering", "ECT401"),
            ("Optical Fiber Communication", "ECT403")
        ],
        8: [
            ("Wireless Systems", "ECT402"),
            ("Seminar & Project Phase II", "ECD416")
        ]
    },
    "EEE": {
        1: [
            ("Group Specific Mathematics - I", "GYMAT101"),
            ("Physics for Engineers", "GYPHT121"),
            ("Introduction to Electrical & Electronics Engineering", "GYEST104")
        ],
        2: [
            ("Group Specific Mathematics - II", "GYMAT201"),
            ("Chemistry for Engineers", "GYCYT122"),
            ("Circuits & Networks", "GYEST203")
        ],
        3: [
            ("Analog Electronics", "EET201"),
            ("DC Machines and Transformers", "EET203")
        ],
        4: [
            ("Digital System Design", "EET202"),
            ("AC Machines & Alternators", "EET204")
        ],
        5: [
            ("Power Systems", "EET301"),
            ("Control Systems", "EET303")
        ],
        6: [
            ("Power Electronics & Drives", "EET302"),
            ("Microprocessors and Microcontrollers", "EET304")
        ],
        7: [
            ("Switchgear and Protection", "EET401"),
            ("Electrical Machine Design", "EET403")
        ],
        8: [
            ("Smart Power Grids", "EET402")
        ]
    },
    "ME": {
        1: [
            ("Group Specific Mathematics - I", "GCMAT101"),
            ("Physics for Engineers", "GCPHT121"),
            ("Engineering Mechanics", "GCEST103")
        ],
        2: [
            ("Group Specific Mathematics - II", "GYMAT201"),
            ("Chemistry for Engineers", "GYCYT122"),
            ("Introduction to Mechanical Engineering", "GCEST104")
        ],
        3: [
            ("Mechanics of Solids", "MET201"),
            ("Fluid Mechanics & Hydraulic Machines", "MET203")
        ],
        4: [
            ("Thermodynamics", "MET202"),
            ("Manufacturing Processes", "MET204")
        ],
        5: [
            ("Heat and Mass Transfer", "MET301"),
            ("Dynamics of Machinery", "MET303")
        ],
        6: [
            ("Design of Machine Elements", "MET302"),
            ("CAD/CAM & Robotics", "MET304")
        ],
        7: [
            ("Mechatronics Systems", "MET401"),
            ("Automobile Engineering", "MET403")
        ],
        8: [
            ("Industrial Operations & Logistics", "MET402")
        ]
    },
    "CE": {
        1: [
            ("Group Specific Mathematics - I", "GCMAT101"),
            ("Physics for Engineers", "GCPHT121"),
            ("Engineering Mechanics", "GCEST103")
        ],
        2: [
            ("Group Specific Mathematics - II", "GYMAT201"),
            ("Chemistry for Engineers", "GYCYT122"),
            ("Introduction to Civil Engineering", "GCEST104")
        ],
        3: [
            ("Mechanics of Materials", "CET201"),
            ("Fluid Mechanics", "CET203"),
            ("Surveying and Geomatics", "CET205")
        ],
        4: [
            ("Structural Analysis", "CET202"),
            ("Geotechnical Engineering I", "CET204")
        ],
        5: [
            ("Design of Reinforced Concrete Structures", "CET301"),
            ("Transportation Engineering", "CET303")
        ],
        6: [
            ("Design of Steel Structures", "CET302"),
            ("Environmental Engineering I", "CET304")
        ],
        7: [
            ("Water Resources Engineering", "CET401"),
            ("Geotechnical Engineering II", "CET403")
        ],
        8: [
            ("Construction Engineering & Project Management", "CET402")
        ]
    }
}

# Preloaded KTU evaluator marking scheme Q&A mapping
ktu_marking_db = [
    {
        "keywords": ["linked list", "circular linked list"],
        "question": "What is a circular linked list? Explain its advantages and disadvantages.",
        "answer": "A circular linked list is a sequence of elements in which every node points to the next node and the last node points back to the first node. Advantages: traversal of the entire list is possible from any starting node; useful for queue implementations. Disadvantages: more complex node insertion/deletion logic; risk of infinite loops if traversal is not handled correctly.\n\n[KTU EVALUATION MARKING SCHEME]:\n- Definition and diagram: 3 Marks (1.5 marks for definition, 1.5 marks for diagram)\n- Advantages: 2 Marks (at least 2 points)\n- Disadvantages: 2 Marks (at least 2 points)\n- Total: 7 Marks"
    },
    {
        "keywords": ["heap sort", "algorithm"],
        "question": "Write the algorithm for Heap Sort and trace it on [15, 5, 20, 1, 10, 8].",
        "answer": "Heap Sort Algorithm: 1. Build a max heap from the input data. 2. Replace the root element with the last element of the heap. 3. Reduce heap size by 1 and heapify the root. 4. Repeat steps 2-3 until heap size is greater than 1.\nTracing: Max heap represents [20, 10, 15, 1, 5, 8]. Sort passes yield sorted array [1, 5, 8, 10, 15, 20].\n\n[KTU EVALUATION MARKING SCHEME]:\n- Algorithm steps/Pseudocode: 4 Marks\n- Heap construction tracing: 3 Marks\n- Heapify process explanation: 2 Marks\n- Final sorted output: 1 Mark\n- Total: 10 Marks"
    },
    {
        "keywords": ["avl", "rotation", "avl tree"],
        "question": "Explain AVL tree rotations with suitable diagrams.",
        "answer": "AVL tree rotations restore balance after insertions or deletions. The four rotations are:\n1. Single Left Rotation (LL): pivot node moves left.\n2. Single Right Rotation (RR): pivot node moves right.\n3. Left-Right Rotation (LR): double rotation; left rotation then right rotation.\n4. Right-Left Rotation (RL): double rotation; right rotation then left rotation.\n\n[KTU EVALUATION MARKING SCHEME]:\n- Explanation of 4 rotations (LL, RR, LR, RL): 4 Marks (1 mark each)\n- Accompanying node diagrams showing balancing: 4 Marks\n- Definition of Balance Factor (BF = height(left) - height(right)): 2 Marks\n- Total: 10 Marks"
    },
    {
        "keywords": ["pigeonhole", "pigeonhole principle"],
        "question": "State and prove Pigeonhole Principle.",
        "answer": "Statement: If n items are put into m containers, with n > m, then at least one container must contain more than one item.\nProof: Assume by contradiction that no container contains more than one item. Then the total number of items would be at most 1 * m = m. Since n > m, this contradicts the assumption that there are n items. Thus, at least one container contains more than one item.\n\n[KTU EVALUATION MARKING SCHEME]:\n- Formal Principle Statement: 2 Marks\n- Mathematical Proof (Contradiction/induction method): 4 Marks\n- Real world application/example: 1 Mark\n- Total: 7 Marks"
    },
    {
        "keywords": ["warshall", "transitive closure"],
        "question": "Find the transitive closure of the relation R = {(1,2), (2,3), (3,4)} using Warshall's Algorithm.",
        "answer": "Warshall's algorithm computes the transitive closure by creating adjacency matrices W0, W1, W2, W3, W4. The final matrix W4 shows connectivity between all reachable nodes, yielding transitive closure R* = {(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)}.\n\n[KTU EVALUATION MARKING SCHEME]:\n- Adjacency matrix setup (W0): 2 Marks\n- Intermediate matrices (W1, W2, W3): 3 Marks (1 mark each)\n- Final transitive closure relation set/matrix: 2 Marks\n- Total: 7 Marks"
    },
    {
        "keywords": ["boolean algebra", "subset"],
        "question": "Show that the set of all subsets of a set forms a Boolean algebra.",
        "answer": "The power set P(S) of a set S forms a Boolean algebra under set union (join), intersection (meet), and complement (not), with empty set as 0 and S as 1. We verify associativity, distributivity, identity, and complement laws.\n\n[KTU EVALUATION MARKING SCHEME]:\n- Definition of operations (union, intersection, complement): 2 Marks\n- Proof of Distributive & Identity Laws: 3 Marks\n- Proof of Complement & Boundedness: 3 Marks\n- Total: 8 Marks"
    },
    {
        "keywords": ["dbms", "normalization"],
        "question": "What is database normalization? Explain 1NF, 2NF, and 3NF with examples.",
        "answer": "Database normalization is the process of organizing attributes in a database to reduce redundancy and dependency.\n- 1NF: Atomic values only. No repeating groups.\n- 2NF: In 1NF and no partial dependencies (non-prime attributes must depend on the whole primary key).\n- 3NF: In 2NF and no transitive dependencies (non-prime attributes must not depend on other non-prime attributes).\n\n[KTU EVALUATION MARKING SCHEME]:\n- Definition of Normalization: 1 Mark\n- 1NF definition & example: 2 Marks\n- 2NF definition & example: 3 Marks\n- 3NF definition & example: 4 Marks\n- Total: 10 Marks"
    },
    {
        "keywords": ["bankers", "deadlock"],
        "question": "What is deadlock? Explain the Banker's algorithm for deadlock avoidance.",
        "answer": "Deadlock is a state where a set of processes are blocked because each process is holding a resource and waiting for another resource. Banker's algorithm manages allocation by verifying if granting a resource keeps the system in a safe state using Allocation, Max, and Available matrices.\n\n[KTU EVALUATION MARKING SCHEME]:\n- Deadlock definition and 4 conditions (Mutual exclusion, hold & wait, no preemption, circular wait): 3 Marks\n- Banker's algorithm data structures (Available, Max, Allocation, Need): 3 Marks\n- Safety algorithm steps/pseudocode: 4 Marks\n- Total: 10 Marks"
    },
    {
        "keywords": ["kmap", "boolean"],
        "question": "Minimize the boolean function using K-Map: F(A,B,C,D) = Σ(0, 2, 5, 7, 8, 10, 13, 15).",
        "answer": "Using a 4-variable Karnaugh Map:\nGroups formed:\n- Quad 1 (0, 2, 8, 10): yields B'D'\n- Quad 2 (5, 7, 13, 15): yields BD\nMinimized expression: F = B'D' + BD\n\n[KTU EVALUATION MARKING SCHEME]:\n- K-Map grid with correct binary labels and cell mappings: 3 Marks\n- Grouping of minterms (identifying quads): 3 Marks\n- Correct simplified product-of-sums or sum-of-products terms: 2 Marks\n- Final expression F = B'D' + BD: 2 Marks\n- Total: 10 Marks"
    },
    {
        "keywords": ["cpu scheduling", "scheduling"],
        "question": "Explain different CPU scheduling algorithms with examples.",
        "answer": "CPU scheduling algorithms allocate CPU time to processes:\n1. FCFS: Non-preemptive, simple, first come first served.\n2. SJF: Selects shortest CPU burst; optimal average wait time.\n3. Round Robin: Preemptive, uses time quantum.\n4. Priority: Executes highest priority process first.\n\n[KTU EVALUATION MARKING SCHEME]:\n- FCFS explanation and Gantt chart: 2 Marks\n- SJF explanation (preemptive/non-preemptive): 3 Marks\n- Round Robin explanation and Gantt chart: 3 Marks\n- Priority scheduling explanation: 2 Marks\n- Total: 10 Marks"
    },
    {
        "keywords": ["soft computing", "hard computing"],
        "question": "What is soft computing? Differentiate between soft computing and hard computing.",
        "answer": "Soft computing is a set of computational techniques (like fuzzy logic, neural networks, genetic algorithms) that tolerate imprecision, uncertainty, and partial truth to achieve tractability and robustness.\nDifferences:\n- Hard computing requires a precise analytical model; Soft computing does not.\n- Hard computing is deterministic; Soft computing allows for probabilistic/approximate solutions.\n- Hard computing is based on binary logic; Soft computing uses multi-valued logic.\n\n[KTU EVALUATION MARKING SCHEME]:\n- Soft computing definition/concept: 3 Marks\n- Hard vs Soft computing comparison table: 5 Marks (at least 5 points)\n- Examples of Soft Computing applications: 2 Marks\n- Total: 10 Marks"
    },
    {
        "keywords": ["software testing", "black box", "white box"],
        "question": "Explain the difference between black box testing and white box testing.",
        "answer": "Black Box Testing: Testing software without knowing its internal code structure or design. Focuses purely on inputs and expected outputs.\nWhite Box Testing: Testing the internal structures, code logic, paths, and flow of the software. Requires programming knowledge.\n\n[KTU EVALUATION MARKING SCHEME]:\n- Black box definition & advantages: 3 Marks\n- White box definition & advantages: 3 Marks\n- Key differences (structure knowledge, test design basis, executor): 4 Marks\n- Total: 10 Marks"
    },
    {
        "keywords": ["distributed computing", "distributed system"],
        "question": "What is a distributed system? Explain the key challenges in distributed system design.",
        "answer": "A distributed system consists of multiple autonomous computers that communicate through a computer network and coordinate their actions by passing messages to appear as a single coherent system.\nKey design challenges:\n1. Heterogeneity: operating systems, networks, hardware.\n2. Openness: ease of extension and re-implementation.\n3. Security: confidentiality, integrity, availability.\n4. Scalability: maintaining performance under increased load.\n5. Failure handling: detection, masking, tolerance.\n\n[KTU EVALUATION MARKING SCHEME]:\n- Definition of Distributed System: 2 Marks\n- Design Challenges: 8 Marks (minimum 4 challenges detailed, 2 marks each)\n- Total: 10 Marks"
    },
    {
        "keywords": ["data mining", "kdd"],
        "question": "Explain the steps involved in KDD (Knowledge Discovery in Databases) process.",
        "answer": "KDD (Knowledge Discovery in Databases) is the process of finding useful, valid, novel, and understandable patterns in data. The steps are:\n1. Selection: retrieving target data.\n2. Preprocessing: cleaning noise and handling missing values.\n3. Transformation: reducing and projecting data into usable forms.\n4. Data Mining: applying algorithms to extract patterns.\n5. Evaluation/Interpretation: visualizing and understanding mined patterns.\n\n[KTU EVALUATION MARKING SCHEME]:\n- Detailed KDD process diagram: 3 Marks\n- Explanation of 5 core phases (Selection, Preprocessing, Transformation, Mining, Evaluation): 5 Marks (1 mark each)\n- Importance of preprocessing step: 2 Marks\n- Total: 10 Marks"
    }
]

# Generate documents dynamically
syllabus_list = []
qps_list = []
questions_list = []

# Generate 2019 Scheme entries
for branch, sems in subjects_2019.items():
    for sem, subjects in sems.items():
        syllabus_doc = {
            "branch": branch,
            "semester": sem,
            "scheme": "2019",
            "subjects": [{"name": name, "code": code} for name, code in subjects]
        }
        syllabus_list.append(syllabus_doc)
        
        for name, code in subjects:
            for yr in [2022, 2023, 2024]:
                q_set = []
                subject_lower = name.lower()
                for item in ktu_marking_db:
                    if any(kw in subject_lower for kw in item["keywords"]):
                        q_set.append(item["question"])
                
                if not q_set:
                    q_set = [
                        f"Explain the basic principles and theory of {name}.",
                        f"Write short notes on industrial applications of {code}.",
                        f"Explain the design process/architecture of a typical {name} system."
                    ]
                
                qps_list.append({
                    "branch": branch,
                    "semester": sem,
                    "scheme": "2019",
                    "subject": name,
                    "year": yr,
                    "exam_type": "Regular/Supplementary",
                    "pdf_url": f"https://example.com/qps/{branch.lower()}_{code.lower()}_{yr}.pdf",
                    "questions": q_set
                })

# Generate 2024 Scheme entries
for branch, sems in subjects_2024.items():
    for sem, subjects in sems.items():
        syllabus_doc = {
            "branch": branch,
            "semester": sem,
            "scheme": "2024",
            "subjects": [{"name": name, "code": code} for name, code in subjects]
        }
        syllabus_list.append(syllabus_doc)
        
        for name, code in subjects:
            for yr in [2024]: # 2024 scheme only has 2024 exam papers
                q_set = []
                subject_lower = name.lower()
                for item in ktu_marking_db:
                    if any(kw in subject_lower for kw in item["keywords"]):
                        q_set.append(item["question"])
                
                if not q_set:
                    q_set = [
                        f"Explain the basic principles and theory of {name}.",
                        f"Write short notes on industrial applications of {code}.",
                        f"Explain the design process/architecture of a typical {name} system."
                    ]
                
                qps_list.append({
                    "branch": branch,
                    "semester": sem,
                    "scheme": "2024",
                    "subject": name,
                    "year": yr,
                    "exam_type": "Regular/Supplementary",
                    "pdf_url": f"https://example.com/qps/{branch.lower()}_{code.lower()}_{yr}.pdf",
                    "questions": q_set
                })

# Seed Q&A DB entries with KTU Evaluation Marking Scheme
for item in ktu_marking_db:
    for branch in branches:
        questions_list.append({
            "question": item["question"].lower(),
            "branch": branch,
            "answer": item["answer"],
            "examples": [],
            "formulas": [],
            "source": "DB",
            "verified": True
        })

# Save to database
syllabus_collection.insert_many(syllabus_list)
qps_collection.insert_many(qps_list)
questions_collection.insert_many(questions_list)

print(f"Successfully seeded STRICT KTU DATABASE:")
print(f"- {len(syllabus_list)} Syllabus entries")
print(f"- {len(qps_list)} Question Paper records (across all semesters, branches, schemes)")
print(f"- {len(questions_list)} Q&A database entries with KTU Evaluation Marking Scheme")
