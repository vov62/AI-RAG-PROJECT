# 🤖 AI-RAG Chatbot Project

This project is a **Question & Answer system** based on **RAG (Retrieval-Augmented Generation)**.  
The user can ask questions in a chat interface, and the system will provide accurate answers **only** based on the uploaded documents (PDFs).

---

## Technologies Used

### Frontend

- **Angular + TypeScript** — modern and interactive user interface.
- Built-in **Dark/Light Mode**.

### Backend

- **Python + Flask** — API server.
- **ChromaDB** — vector database for storing and retrieving document embeddings.
- **OpenAI** — large language models (LLMs) used for natural language
  understanding and answer generation model.
- **LangChain** — orchestration and RAG logic.

### Deployment

- **AWS CLOUD** - hosting the application.
- **Docker & Docker-compose** - containerized deployment on an EC2 instance.

  LIVE - coming soon.

---

## Project Features

- Upload multiple PDF documents.
- Search and query based on **relevant context** from the documents.
- AI answers only based on the documents — no hallucinations.
- Smart conversation memory — the assistant remembers previous questions in  
  the chat.
- Option to **rephrase user queries with AI** before sending.

---

## Screenshots

## <img width="700" height="auto" alt="image" src="https://github.com/user-attachments/assets/0b2c47f3-5ab3-4282-a50c-b3973df7ff78" />

<br>
<img width="700" height="auto" alt="1" src="https://github.com/user-attachments/assets/90840bfa-d8cd-45dc-a25c-e3323424ffa1" />

## Getting Started

### Setup

Clone the repository:

```bash
git clone https://github.com/vov62/AI-RAG-Project.git
cd AI-RAG_Chromadb-Project
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

create .env file with your OPENAI API keys:

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

## Deployment on AWS EC2

This project was deployed on an AWS EC2 instance using Docker Compose, and made publicly accessible via a static Elastic IP.

### Launch an EC2 Instance

First i created a new EC2 Instance on AWS.

Then i connect to the ec2 instance via ssh:

```
ssh -i "your-key.pem" ubuntu@<EC2-PUBLIC-IP>
```

Install Docker and Docker Compose:

```
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
```

Clone My Project From Github:

```
git clone https://github.com/vov62/AI-RAG-Project.git
cd AI-RAG_Chromadb-Project
```

create .env file inside the project root and enter my OPENAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

build and run with docker-compose:

```
docker-compose up --build -d
```

This will launches 2 containers:

- **Frontend Container** (Angular + Nginx)
- **Backend Container** (Flask + OPENAI)
