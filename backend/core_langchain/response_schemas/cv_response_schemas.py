"""
Module to specify response schemas for langchain CV chains.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class CVResponseSchema(BaseModel):
    name: str = Field(description="Full name of the candidate")
    contact: Optional[str] = Field(
        description="Email and phone number if available"
    )
    summary: Optional[str] = Field(
        description="Summary of the candidate's career and skills"
    )
    skills: Optional[str] = Field(
        description="List of key skills, both technical and soft skills"
    )
    experience: Optional[str] = Field(
        description="Work experience including job title, company, dates, and responsibilities"
    )
    project: Optional[str] = Field(
        description="Projects the candidate has worked on, including the name of the project, the role, and the responsibilities"
    )
    education: Optional[str] = Field(
        description="Education history, degrees, institutions, and graduation years"
    )
    certifications: Optional[str] = Field(
        description="Any certifications or licenses listed"
    )
    languages: Optional[str] = Field(
        description="Languages the candidate knows"
    )


class SkillsGapSchema(BaseModel):
    general_recommendations: str = Field(
        description="Overview recommendations to improve the CV to match the job description"
    )
    match_score: float = Field(
        description="Matching score between 0 and 1 of the CV skills and job description",
        ge=0.0,
        le=1.0,
    )
    missing_skills: List[str] = Field(
        description="Missing skills from the CV to match the job description"
    )
    matched_skills: List[str] = Field(
        description="Matched skills from the CV to the job description"
    )
    job_description_ats_skills_extracted: Dict[str, List[str]] = Field(
        description="Extract related keywords (exactly 20 keywords) from the job description that is most important to the position to put into a ATS screening system. Please categorize them based on must have and nice to have."
    )


class CVMainBulletPointsSchema(BaseModel):
    main_bullet_points: List[str] = Field(
        description="List of extracted main bullet points from the CV"
    )


class CVImprovedBulletPointsSchema(BaseModel):
    new_cv_bullet_points: List[str] = Field(
        description="New CV bullet points to match the job description."
    )


class ATSKeywordsSchema(BaseModel):
    ats_keywords_included: List[str] = Field(
        description="List of all ATS keywords included in the new CV bullet points (both already in the bullet points and newly added)"
    )
