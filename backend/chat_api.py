import pickle
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.embeddings import FakeEmbeddings  # Replace with real if available

# Load .env variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Load face database
DB_PATH = '../server/face_db.pkl'
with open(DB_PATH, 'rb') as f:
    face_db = pickle.load(f)

# Convert face DB to text documents
documents = []
for name in set(face_db.get('names', [])):
    if not name or not isinstance(name, str) or name.strip() == '':
        continue
    name = name.strip()
    count = face_db['names'].count(name)
    last_date = None
    if 'dates' in face_db:
        dates_for_name = [
            face_db['dates'][i] for i, n in enumerate(face_db['names'])
            if n == name and face_db['dates'][i]
        ]
        if dates_for_name:
            last_date = max(dates_for_name)
    doc = f"{name} registered {count} time(s)."
    if last_date:
        doc += f" Last registration was on {last_date}."
    documents.append(doc)

# Set up embeddings and vector store
embedding = FakeEmbeddings(size=1536)  # Replace with actual embedding support when Groq provides
db = FAISS.from_texts(documents, embedding)

# Load LLM (Groq)
llm = ChatGroq(api_key=GROQ_API_KEY, model="llama3-70b-8192")
qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

# Define input/output schemas
class ChatQuery(BaseModel):
    query: str

@app.post("/chat")
def chat_with_face_data(payload: ChatQuery):
    try:
        answer = qa.run(payload.query)
        return {"response": answer}
    except Exception as e:
        return {"error": str(e)}
