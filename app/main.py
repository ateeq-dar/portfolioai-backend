from fastapi import FastAPI
from pydantic import BaseModel
from app.database import SessionLocal, init_db
from app.models import Profile, Skill, Project, ChatLog
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# ✅ CORS MUST be added immediately after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ateeqportfolioai.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Initialize DB after middleware setup
init_db()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "Backend Running"}


@app.post("/chat")
def chat(request: ChatRequest):

    db = SessionLocal()

    try:
        profile = db.query(Profile).first()
        skills = db.query(Skill).all()
        projects = db.query(Project).all()

        resume_context = f"""
Name: {profile.name}
Title: {profile.title}
Summary: {profile.summary}

Skills:
{', '.join([skill.skill_name for skill in skills])}

Projects:
{chr(10).join([f"{p.title} - {p.full_description}" for p in projects])}
"""

        prompt = f"""
You are an AI assistant answering strictly based on this resume:

{resume_context}

If the question is not related to the resume, politely say you do not have that information.

Question:
{request.message}
"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
            },
        )

        result = response.json()

        if "choices" not in result:
            return {"answer": "Unable to generate response at the moment."}

        answer = result["choices"][0]["message"]["content"]

        log = ChatLog(question=request.message, answer=answer)
        db.add(log)
        db.commit()

        return {"answer": answer}

   except Exception as e:
    return {"answer": f"DEBUG ERROR: {str(e)}"}

    finally:
        db.close()
