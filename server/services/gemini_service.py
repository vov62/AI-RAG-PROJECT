# server/services/gemini_service.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# טוען משתני סביבה
load_dotenv()

# מקבל את ה-API Key של Gemini מהסביבה
GEMINI_API_KEY = os.getenv("CHROMA_GOOGLE_GENAI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing! Please set CHROMA_GOOGLE_GENAI_API_KEY in your .env file.")

# הגדרת המפתח עבור Gemini
genai.configure(api_key=GEMINI_API_KEY)

# שם המודל שבו נשתמש
DEFAULT_MODEL = "gemini-2.0-flash"


def get_gemini_answer(prompt, model_name=DEFAULT_MODEL, temperature=0.2):
    """
    שולח Prompt ל-Gemini ומחזיר תשובה טקסטואלית.
    
    :param prompt: הטקסט שברצוננו לשלוח למודל
    :param model_name: שם המודל (ברירת מחדל gemini-2.0-flash)
    :param temperature: שליטה על יצירתיות התשובה
    :return: תשובת המודל כטקסט
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature
            )
        )

        return response.text.strip() if response.text else "לא התקבלה תשובה ממודל Gemini."
    
    except Exception as e:
        print(f"[Gemini Error] {str(e)}")
        return "אירעה שגיאה בעת תקשורת עם Gemini."


def summarize_context(context, user_query, model_name=DEFAULT_MODEL):
    """
    דוגמה לפונקציה מתקדמת: מסכמת את הקונטקסט לפני הצגת תשובה למשתמש.
    
    :param context: המידע שנשלף מ-ChromaDB
    :param user_query: השאלה של המשתמש
    :return: סיכום מתומצת של המידע
    """
    prompt = f"""
    סכם את הקטעים הבאים בעברית ברורה וקצרה,
    כך שהתשובה תענה על השאלה הבאה:
    
    שאלה: {user_query}
    
    קונטקסט:
    {context}
    """

    return get_gemini_answer(prompt, model_name=model_name, temperature=0.1)
