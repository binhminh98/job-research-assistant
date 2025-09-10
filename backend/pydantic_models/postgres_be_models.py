from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    inserted_at = Column(DateTime, nullable=False, server_default=func.now())
    inserted_by = Column(
        String, nullable=False, server_default=func.session_user()
    )
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    updated_by = Column(
        String,
        server_default=func.session_user(),
        onupdate=func.session_user(),
    )

    cvs = relationship("CVData", back_populates="user")
    cv_analysis_jobs = relationship("CVAnalysisJobs", back_populates="user")


class CVData(Base):
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
    inserted_at = Column(DateTime, nullable=False, server_default=func.now())
    inserted_by = Column(
        String, nullable=False, server_default=func.session_user()
    )
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    updated_by = Column(
        String,
        server_default=func.session_user(),
        onupdate=func.session_user(),
    )

    user = relationship("User", back_populates="cvs")
    cv_analysis_jobs = relationship("CVAnalysisJobs", back_populates="cv")


class CVAnalysisJobs(Base):
    __tablename__ = "cv_analysis_jobs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cv_id = Column(Integer, ForeignKey("cv_data.id"), nullable=False)
    company_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    raw_analysis_result = Column(JSONB)

    inserted_by = Column(
        String, nullable=False, server_default=func.session_user()
    )
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    updated_by = Column(
        String,
        server_default=func.session_user(),
        onupdate=func.session_user(),
    )

    user = relationship("User", back_populates="cv_analysis_jobs")
    cv = relationship("CVData", back_populates="cv_analysis_jobs")
