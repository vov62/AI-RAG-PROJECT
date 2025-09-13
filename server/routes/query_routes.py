from flask import Blueprint, jsonify, request
from services.chroma_service import load_pdfs_into_chroma, query_documents
import google.generativeai as genai
from services.gemini_service import get_gemini_answer


# === 1. טעינת המסמכים עם הגנה מטעויות ===
try:
    load_pdfs_into_chroma()
    print("PDFs loaded successfully into ChromaDB.")
except Exception as e:
    print(f"Error loading PDFs into ChromaDB: {e}")

# === 2. יצירת ה-Blueprint ===
query_bp = Blueprint("query_bp", __name__)

# === 3. בריאות השרת ===
@query_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Flask API is running!"})

# === 4. קבלת שאלה מהמשתמש ===
@query_bp.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "query text not provided"}), 400

    # 4.1 שליפת המסמכים הרלוונטיים מ-ChromaDB
    chroma_result = query_documents(user_query,n_results=5)
    retrieved_texts = chroma_result.get("documents", [[]])[0]

    if not retrieved_texts:
        return jsonify({
            "query_received": user_query,
            "answer": "no relevant information found in the documents."
        })


    top_relevant = "\n\n".join(retrieved_texts)

    # 4.2 יצירת תשובה עם Gemini
    prompt = f"""
            You are a document-based assistant.
            Answer the following question using ONLY the information provided in the documents.
            If the answer is not in the documents, respond: 
            "אין לי מספיק מידע לענות על זה. נא נסח את שאלתך מחדש "

             User question: {user_query}

            Relevant documents:
            {top_relevant}
            """
    answer = get_gemini_answer(prompt)

    # 4.3 החזרת תשובה לאנגולר
    return jsonify({
        "query_received": user_query,
        "retrieved_docs_count": len(retrieved_texts),
        "answer": answer
    })