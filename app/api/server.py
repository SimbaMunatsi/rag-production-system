from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.service import create_rag_pipeline


app = FastAPI()

rag = create_rag_pipeline()


class Question(BaseModel):
    query: str


@app.post("/ask")
def ask_question(question: Question):

    result = rag.run(question.query)

    return result