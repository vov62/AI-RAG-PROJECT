# server/services/rag_pipeline.py
from services.chroma_service import query_documents
from services.gemini_service import get_gemini_answer

def answer_query(user_query):
    # 1. חיפוש במסמכים
    results = query_documents(user_query, n_results=5)
    retrieved_docs = results["documents"][0]

    # 2. יצירת הקשר לג'מיני
    context = "\n\n".join(retrieved_docs)

    prompt = f"""
    ענה על השאלה הבאה בעברית תוך שימוש במידע שמופיע בקונטקסט בלבד.
    אם אין תשובה בקונטקסט, אמור "לא מצאתי מידע רלוונטי".

    קונטקסט:
    {context}

    שאלה:
    {user_query}
    """

    # 3. קבלת תשובה מג'מיני
    gemini_answer = get_gemini_answer(prompt)

    return gemini_answer, retrieved_docs
