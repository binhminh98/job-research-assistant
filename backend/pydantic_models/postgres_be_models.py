from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship

BASE = declarative_base()


class User(BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Establish a relationship with the CV data
    cvs = relationship("CVData", back_populates="user")


class CVData(BASE):
    __tablename__ = "cv_data"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)
    raw_text = Column(String, nullable=False)
    extracted_text = Column(JSONB, nullable=False)
    contact = Column(String)
    certifications = Column(String)
    skills = Column(String)
    summary = Column(String)
    languages = Column(String)
    education = Column(JSONB)
    experience = Column(JSONB)

    # Establish a relationship with the User
    user = relationship("User", back_populates="cvs")
