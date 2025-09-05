"""
Module to specify response schemas for langchain company parser chains.
"""

from pydantic import BaseModel, Field


class CompanyInfoSchema(BaseModel):
    company_name: str = Field(description="Full name of the company")
    summarized_company_values: str = Field(
        description="Summarized company values and culture in 30-35 bullet points"
    )
