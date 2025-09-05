import os
import chromadb
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# === הגדרות בסיס ===
CHROMA_DB_DIR = "./server/chroma_db"  # מיקום לשמירת בסיס הנתונים
PDF_DIR = "./data"             # תיקייה שבה שמורים ה-PDFים
COLLECTION_NAME = "knowledge_base"    # שם הקולקציה הראשית

# === פונקציות עזר ===

def get_embedding_function():
    """
    יוצר פונקציית Embedding - אחראית להפוך טקסט למספרים
    כדי ש-ChromaDB יוכל לבצע חיפוש סמנטי.
    """
    return SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

def get_or_create_collection():
    """יוצר או מחזיר collection קיימת בשם שקבענו."""
    """יוצר חיבור פרסיסטנטי ל-ChromaDB (שנשמר בדיסק)."""
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function()
    )

# === שלב 1: טעינת PDFים לתוך ChromaDB ===
def load_pdfs_into_chroma():
    """
    קורא את כל ה-PDFים בתיקייה,
    מפרק אותם לטקסטים קטנים (chunks),
    ומכניס אותם לתוך ChromaDB.
    """
    collection = get_or_create_collection()
    print("Loading PDFs into ChromaDB...")

    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            file_path = os.path.join(PDF_DIR, filename)
            print(f"Processing {filename}...")

            # קריאת כל הדפים מה-PDF
            reader = PdfReader(file_path)
            pdf_texts = [page.extract_text() for page in reader.pages if page.extract_text()]

            # חיבור הטקסט כולו
            full_text = "\n\n".join(pdf_texts)

            # פיצול הטקסט ל-chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100
            )
            chunks = splitter.split_text(full_text)

            # יצירת IDs ייחודיים
            ids = [f"{filename}_{i}" for i in range(len(chunks))]

            # הוספה ל-collection
            collection.add(documents=chunks, ids=ids)

    print(f"Finished loading PDFs. Total documents in DB: {collection.count()}")

# === שלב 2: חיפוש במסמכים ===
def query_documents(query, n_results=5):
    """
    מבצע חיפוש במסמכים לפי שאלה של המשתמש.
    """
    collection = get_or_create_collection()
    return collection.query(query_texts=[query], n_results=n_results)

# === שלב 3: איפוס כללי (אם רוצים להתחיל מחדש) ===
# def reset_collection():
#     """מוחק את כל הקולקציה ומתחיל מחדש."""
#     client = get_chroma_client()
#     client.delete_collection(name=COLLECTION_NAME)
#     print("Collection has been reset!")
