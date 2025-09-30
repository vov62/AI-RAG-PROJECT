# 🤖 AI-RAG Chatbot Project

This project is a **Question & Answer (Q&A) system** based on **RAG (Retrieval-Augmented Generation)**.  
The user can ask questions in a chat interface, and the system will provide accurate answers **only** based on the uploaded documents (PDFs).

---

## 🚀 Technologies Used

### Frontend

- [Angular](https://angular.dev/) — modern and interactive user interface.
- [TypeScript](https://www.typescriptlang.org/) — strong typing and clean code.
- [TailwindCSS / Custom CSS] — lightweight and modern design.
- Built-in **Dark/Light Mode**.
- Support for **emojis** and user-friendly UX.

### Backend

- [Python](https://www.python.org/) + [Flask](https://flask.palletsprojects.com/) — fast and flexible API server.
- [ChromaDB](https://www.trychroma.com/) — vector database for storing and retrieving document embeddings.
- [OpenAI](https://openai.com/) — large language models (LLMs) used for natural language understanding and answer generation.
- [LangChain](https://www.langchain.com/) — orchestration and RAG logic.

---

## 📂 Project Features

- Upload multiple PDF documents.
- Search and query based on **relevant context** from the documents.
- AI answers only based on the documents — no hallucinations.
- Smart conversation memory — the assistant remembers previous questions in the chat.
- Option to **rephrase user queries with AI** before sending.
- Error handling with clear messages in the UI.

---

## 📸 Screenshots

> Add screenshots here once uploaded (e.g. chat interface, light/dark mode examples).

Example:  
![Chat UI Screenshot](./images/chat-ui.png)

---

## ⚡ Getting Started

### Prerequisites

- Node.js (for Angular frontend)
- Python 3.10+
- Virtual environment for Python dependencies

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/vov62/AI-RAG-Project.git
   cd AI-RAG-Project
   ```

Install server dependencies:
cd server
pip install -r requirements.txt

Install frontend dependencies:
cd client
npm install

create .env file with your API AI keys
OPENAI_API_KEY=your_key_here

Run the backend(Flask):
cd server
python app.js

Run the frontend(Angular):
cd client
npm start

```

```
