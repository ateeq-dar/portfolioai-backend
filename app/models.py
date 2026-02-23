from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from .database import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    title = Column(String(150))
    summary = Column(Text)
    phone = Column(String(20))
    email = Column(String(150))
    location = Column(String(150))
    portfolio_link = Column(String(255))


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(100))
    category = Column(String(100))


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    short_description = Column(String(255))
    full_description = Column(Text)
    tech_stack = Column(String(255))


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())