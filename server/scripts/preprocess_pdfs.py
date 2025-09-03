# server/scripts/preprocess_pdfs.py
import os
from utils.pdf_utils import extract_text_from_pdf
from services.chroma_service import add_documents, reset_collection

PDF_FOLDER = "./server/pdf_files"

def preprocess_pdfs():
    # מאפס את כל המאגר לפני טעינה חדשה
    reset_collection()

    for file_name in os.listdir(PDF_FOLDER):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(PDF_FOLDER, file_name)
            print(f"Processing {file_name}...")

            # חילוץ טקסט וחלוקה לקטעים
            text_chunks = extract_text_from_pdf(file_path)

            # יוצרים מזהי ייחודיים לקטעים
            ids = [f"{file_name}-{i}" for i in range(len(text_chunks))]
            metadatas = [{"source": file_name} for _ in range(len(text_chunks))]

            # מוסיפים ל-Chroma
            add_documents(documents=text_chunks, metadatas=metadatas, ids=ids)

    print("Preprocessing complete! All PDFs indexed.")

if __name__ == "__main__":
    preprocess_pdfs()
