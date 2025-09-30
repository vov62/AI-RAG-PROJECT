# 🤖 AI-RAG Chatbot Project

This project is a **Question & Answer system** based on **RAG (Retrieval-Augmented Generation)**.  
The user can ask questions in a chat interface, and the system will provide accurate answers **only** based on the uploaded documents (PDFs).

---

## Technologies Used

### Frontend

- [Angular] + TypeScript — modern and interactive user interface.
- [TypeScript](https://www.typescriptlang.org/) — strong typing and clean code.
- Custom CSS— lightweight and modern design.
- Built-in **Dark/Light Mode**.

### Backend

- [Python]+ [Flask] — fast and flexible API server.
- [ChromaDB]— vector database for storing and retrieving document embeddings.
- [OpenAI] — large language models (LLMs) used for natural language understanding and answer generation.
- [LangChain] — orchestration and RAG logic.

---

## Project Features

- Upload multiple PDF documents.
- Search and query based on **relevant context** from the documents.
- AI answers only based on the documents — no hallucinations.
- Smart conversation memory — the assistant remembers previous questions in the chat.
- Option to **rephrase user queries with AI** before sending.

---

## Screenshots

## <img width="700" height="auto" alt="image" src="https://github.com/user-attachments/assets/0b2c47f3-5ab3-4282-a50c-b3973df7ff78" />

<br>
<img width="700" height="auto" alt="1" src="https://github.com/user-attachments/assets/90840bfa-d8cd-45dc-a25c-e3323424ffa1" />

## Getting Started

### Prerequisites

- Node.js (for Angular frontend)
- Python 3.10+
- Virtual environment for Python dependencies

### Setup

Clone the repository:

```bash
git clone https://github.com/vov62/AI-RAG-Project.git
cd AI-RAG-Project
```

Install server dependencies:

```
cd server
pip install -r requirements.txt
```

Install frontend dependencies:

```
cd client
npm install
```

create .env file with your API AI keys:

```
OPENAI_API_KEY=your_key_here
```

Run the backend:

```
cd server
python app.js
```

Run the frontend:

```
cd client
npm start
```
