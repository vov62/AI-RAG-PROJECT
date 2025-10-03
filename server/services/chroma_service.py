import os
import chromadb
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

CHROMA_DB_DIR = "./server/chroma_db"  # מיקום לשמירת בסיס הנתונים
PDF_DIR = "./data"             # תיקייה שבה שמורים ה-PDFים
COLLECTION_NAME = "knowledge_base"    # שם הקולקציה הראשית

# יצירת פונקציית EMBEDDING
def get_embedding_function():
    return OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-large"       
    )

# יוצר או מחזיר COLLECTION
def get_or_create_collection():
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function()
    )

#  טעינת PDF לתוך ChromaDB
def load_pdfs_into_chroma():
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
                chunk_overlap=200
            )
            chunks = splitter.split_text(full_text)

            # יצירת IDs ייחודיים
            ids = [f"{filename}_{i}" for i in range(len(chunks))]

            # הוספה ל-collection
            collection.add(documents=chunks, ids=ids)

    print(f"Finished loading PDFs. Total documents in DB: {collection.count()}")

#  חיפוש במסמכים 
def query_documents(query, n_results=8):
    collection = get_or_create_collection()
    return collection.query(query_texts=[query], n_results=n_results)
