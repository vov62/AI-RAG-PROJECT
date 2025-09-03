# server/services/chroma_service.py
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import os

# קובץ זה מטפל בכל מה שקשור ל-ChromaDB
# אחראי על יצירת חיבור, קריאת מסמכים, הוספה ושאילתות

# מיקום שבו נשמור את הדאטה בצורה פרסיסטנטית
CHROMA_DB_DIR = "./server/chroma_db"

# שם הקולקציה הראשית
COLLECTION_NAME = "knowledge_base"


# יצירת פונקציית Embedding
def get_embedding_function():
    """
    יוצרת פונקציה ליצירת embeddings.
    כאן בחרנו ב-Sentence Transformers multilingual,
    כדי לתמוך גם בעברית וגם באנגלית.
    """
    return SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

# חיבור ל-ChromaDB
def get_chroma_client():
    """
    יוצר חיבור ל-ChromaDB עם אפשרות שמירה פרסיסטנטית בדיסק.
    """
    return chromadb.PersistentClient(path=CHROMA_DB_DIR)

# יצירת קולקציה אם לא קיימת
def get_or_create_collection():
    """
    מוודא שקיימת קולקציה ראשית ב-ChromaDB,
    ואם לא - יוצרת אותה.
    """
    chroma_client = get_chroma_client()
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function()
    )

# הוספת מסמכים חדשים
def add_documents(documents, metadatas=None, ids=None):
    """
    מוסיפה מסמכים חדשים ל-collection.

    :param documents: רשימת טקסטים (chunks)
    :param metadatas: רשימת metadata (למשל {"source": "contract.pdf"})
    :param ids: מזהים ייחודיים
    """
    collection = get_or_create_collection()
    collection.add(documents=documents, metadatas=metadatas, ids=ids)

# ביצוע שאילתה
def query_documents(query, n_results=5):
    """
    מבצע חיפוש במסמכים לפי השאילתה של המשתמש.

    :param query: טקסט החיפוש
    :param n_results: כמה תוצאות להביא
    :return: תוצאות Chromadb
    """
    collection = get_or_create_collection()
    return collection.query(query_texts=[query], n_results=n_results)

# מחיקת הקולקציה (למטרות reset)
def reset_collection():
    """
    מוחק לחלוטין את הקולקציה הראשית.
    שימושי אם רוצים לבנות את המאגר מחדש.
    """
    chroma_client = get_chroma_client()
    chroma_client.delete_collection(name=COLLECTION_NAME)
