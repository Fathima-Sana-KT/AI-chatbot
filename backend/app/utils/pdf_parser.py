import os
import fitz  # PyMuPDF

def extract_curriculum_text(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"⚠ PDF file not found at path: {pdf_path}")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def save_curriculum_to_txt(pdf_path, txt_path):
    content = extract_curriculum_text(pdf_path)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)

