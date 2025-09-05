"""
Module to specify response schemas for langchain JD chains.
"""

from pydantic import BaseModel, Field


class JobDescriptionSchema(BaseModel):
    company_name: str = Field(description="Full name of the company")
    job_title: str = Field(
        description="Title of the job, only extract real job title, not just the title of the page"
    )
    job_description: str = Field(description="Description of the job posting")
