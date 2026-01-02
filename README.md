# 🎫 SmartDesk AI
### Intelligent IT Support & Ticket Automation System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-47A248)
![AI](https://img.shields.io/badge/AI-LangChain%20%7C%20Groq-orange)

## 🚀 Live Demo
**👉 [Try the App Here](https://smartdesk-ai.streamlit.app/)** *(Note: The backend runs on a free instance and may take ~50s to wake up on the first request.)*

---

## 📖 Overview
**SmartDesk AI** is an intelligent full-stack helpdesk platform designed to streamline IT support workflows. It leverages **Large Language Models (LLMs)** and **Retrieval-Augmented Generation (RAG)** to automatically categorize tickets, assign priority, and generate instant resolution drafts for support agents.

Unlike traditional ticketing systems, SmartDesk AI learns from historical solutions to provide context-aware answers, reducing the "Mean Time to Resolve" (MTTR) for support teams.

## ✨ Key Features
* **🤖 AI-Powered Triage:** Automatically detects ticket **Category** (Hardware, Software, Network) and **Priority** (High, Medium, Low) using NLP.
* **🧠 RAG Knowledge Base:** Retrieves similar past tickets and solutions using vector embeddings (HuggingFace) to suggest accurate fixes.
* **⚡ Automated Drafts:** Generates polite, professional, and technical email replies for admins to review and send.
* **📊 Admin Dashboard:** Visual analytics for ticket volume, status tracking, and one-click AI resolution.
* **🔐 Role-Based Access:** Secure admin login to manage and close tickets.

---

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit (Python) |
| **Backend** | FastAPI (Python) |
| **Database** | MongoDB Atlas (Cloud NoSQL) |
| **AI / LLM** | Groq API (Llama 3), LangChain |
| **Embeddings** | HuggingFace (`sentence-transformers`) |
| **Deployment** | Render (Backend) + Streamlit Cloud (Frontend) |

---

## ⚙️ Architecture
1.  **User Submission:** User submits a ticket via the Streamlit interface.
2.  **Preprocessing:** FastAPI receives data; AI analyzes sentiment and keywords to assign Priority/Category.
3.  **Vector Search:** The system converts the issue description into embeddings and searches MongoDB for similar solved tickets.
4.  **Generation:** The LLM (via Groq) combines the new issue + retrieved context to generate a suggested solution.
5.  **Admin Review:** Admin reviews the AI draft, modifies if needed, and marks the ticket as "Closed".

---

## 💻 Local Installation
If you want to run this locally:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/shinewithsachin/smartdesk-ai.git](https://github.com/shinewithsachin/smartdesk-ai.git)
    cd smartdesk-ai
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**
    Create a `.env` file and add:
    ```env
    MONGO_URI=your_mongodb_connection_string
    DB_NAME=support_system
    GROQ_API_KEY=your_groq_api_key
    ```

4.  **Run the Backend**
    ```bash
    uvicorn app.main:app --reload
    ```

5.  **Run the Frontend** (In a new terminal)
    ```bash
    streamlit run streamlit_app.py
    ```

---

## 📸 Screenshots
### 1. Ticket Dashboard
![Dashboard](Screenshots/Screenshot%202026-01-02%20140751.png)

### 2. Admin Panel
![Admin Panel](Screenshots/Screenshot%202026-01-02%20140731.png)

### 3. AI Resolution
![AI Reply](Screenshots/Screenshot%202026-01-02%20140657.png)

---

## 📬 Contact
Created by **[Your Name]** * [LinkedIn Profile](https://www.linkedin.com/in/sachin-iiitg/)
* [GitHub Profile](https://github.com/shinewithsachin)
* [My Portfolio](https://build-your-portfolio-ceetocb.gamma.site/untitled-lsuym)