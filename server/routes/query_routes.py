from flask import Blueprint, jsonify, request
from services.chroma_service import load_pdfs_into_chroma, query_documents
# from services.gemini_service import get_gemini_answer, get_openai_answer
from services.gemini_service import get_openai_answer


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
    user_query = data.get("query", "").strip() 
  
    if not user_query:
        return jsonify({"error": "query text not provided"}), 400

    # 4.1 שליפת המסמכים הרלוונטיים מ-ChromaDB
    try:
        chroma_result = query_documents(user_query, n_results=5)
        retrieved_texts = chroma_result.get("documents", [[]])[0]
    except Exception as e:
        return jsonify({"error": f"Failed to query ChromaDB: {str(e)}"}), 500

    # chroma_result = query_documents(user_query,n_results=5)

    if not retrieved_texts:
        return jsonify({
            "query_received": user_query,
            "answer": "no relevant information found in the documents."
        }),404


    # 4.2 יצירת תשובה עם Gemini
    top_relevant = "\n\n".join(retrieved_texts)
    prompt = f"""
            You are an experienced, professional, and courteous virtual assistant that helps users answer questions **only** based on the provided documents.

            Instructions:
            - Always respond **only in Hebrew**, using clear and respectful language.
            - Organize your response in a structured way:
            - If there are multiple points — use bullet points.
            - If it's a general explanation — use short, clear paragraphs.
            - If the information is not found in the documents, respond:
            "אין לי מספיק מידע לענות על זה מתוך המסמכים. נא נסח את שאלתך מחדש."
            - **Never fabricate information** that does not appear in the documents

            User question: {user_query}

            Relevant documents:
            {top_relevant}
            """
    try:
        # answer = get_gemini_answer(prompt)
        answer = get_openai_answer(prompt)
    except Exception as e:
        return jsonify({"error": f"Gemini API error: {str(e)}"}), 502

    # 4.3 החזרת תשובה לאנגולר
    return jsonify({
        "query_received": user_query,
        "retrieved_docs_count": len(retrieved_texts),
        "answer": str(answer)
    })


# rephrase route
@query_bp.route("/rephrase", methods=["POST"])
def rephrase_query():
    data = request.get_json()
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "query text is missing"}), 400
    
    prompt = f"""
            You are an assistant that specializes in rewriting Hebrew sentences clearly and accurately.

            Your task:
            - Rewrite the following user question in **Hebrew**.
            - Keep the **original meaning** exactly the same.
            - Make the question **clearer, more natural, and grammatically correct**.
            - Do NOT translate to another language.
            - Respond **only** with the rewritten question, without explanations or extra text.

            User question: "{user_query}"
            """
    
    try:
        # rephrased = get_gemini_answer(prompt)
        rephrased = get_openai_answer(prompt)
        
        return jsonify({
            "original_query": user_query,
            "rephrased_query": rephrased
        })
    except Exception as e:
        return jsonify({
            "error":"Failed to rephrase query",
            "details": str(e)
        }), 500