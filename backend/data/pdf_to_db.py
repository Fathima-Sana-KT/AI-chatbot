import requests
import pdfplumber
import pandas as pd
import sqlalchemy
from pymongo import MongoClient
import os

# PostgreSQL Database Config
POSTGRES_URI = "postgresql://postgres:1234ad@localhost:5432/ktudb"


# MongoDB Config
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "ktudb"
MONGO_COLLECTION = "syllabus"

# Directory to store PDFs
PDF_DIR = "ktu_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# Function to download PDFs
def download_pdf(url):
    filename = os.path.join(PDF_DIR, url.split("/")[-1])
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Downloaded: {filename}")
    return filename

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_data.append(page.extract_text())
    return "\n".join(text_data)

# Function to process and clean extracted text
import re

import re

def process_syllabus_data(text):
    """
    Extracts structured syllabus topics and details from raw PDF text.
    """
    lines = text.split("\n")
    data = []
    
    for i in range(len(lines) - 1):
        topic = lines[i].strip()
        description = lines[i + 1].strip()

        # Ensure valid topics are stored
        if (
            len(topic) > 3 
            and not topic.isupper()  # Avoid large section headings
            and not re.search(r'\d{2,}', topic)  # Ignore table numbers
        ):
            data.append({"topic": topic, "details": description})  # Store with "topic" key
    
    return data

# Function to save data to PostgreSQL
def save_to_postgresql(data):
    engine = sqlalchemy.create_engine(POSTGRES_URI)
    df = pd.DataFrame(data)
    df.to_sql("syllabus", con=engine, if_exists="replace", index=False)
    print("Data saved to PostgreSQL")

# Function to save data to MongoDB
def save_to_mongodb(data):
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    collection.insert_many(data)
    print("Data saved to MongoDB")

# Main Function
def main():
    pdf_links = [
        "https://vidyatcklmr.ac.in/admin/upload/pdf/1629672737BTech2019Curriculum.pdf",
        "https://www.thejusengg.com/ckfinder/userfiles/files/KTU%20Curriculum%202024.pdf",
        # Add other branch syllabus links here
    ]

    for pdf_url in pdf_links:
        pdf_path = download_pdf(pdf_url)
        text = extract_text_from_pdf(pdf_path)
        structured_data = process_syllabus_data(text)
        save_to_postgresql(structured_data)
        save_to_mongodb(structured_data)

if __name__ == "__main__":
    main()
