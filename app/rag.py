import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


try:
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("✅ Groq + HuggingFace Connected Successfully")

except Exception as e:
    print(f"❌ Error connecting to AI Provider: {e}")
    llm = None
    embeddings = None



qa_chain = None

if llm and embeddings:
    try:
        loader = TextLoader("app/knowledge_base.txt", encoding="utf-8")
        documents = loader.load()

        vector_store = FAISS.from_documents(documents, embeddings)
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        template = """
        You are a helpful IT support agent. 
        Context: {context}
        Ticket: {question}
        
        Draft a polite Email Reply:
        """
        prompt = PromptTemplate.from_template(template)

        qa_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        print("✅ RAG Pipeline Built Successfully")

    except Exception as e:
        print(f"❌ Error building pipeline: {e}")


def generate_response(ticket_description: str) -> str:
    if not qa_chain:
        return "AI System is offline."
    try:
        return qa_chain.invoke(ticket_description).strip()
    except Exception as e:
        return f"Error: {str(e)}"