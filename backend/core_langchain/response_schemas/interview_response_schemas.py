"""
Module to specify response schemas for langchain interview chains.
"""

from typing import List

from pydantic import BaseModel, Field


class InterviewQuestionsGeneratorSchema(BaseModel):
    general_questions: List[str] = Field(
        description="List of general questions generated."
    )
    behavioral_questions: List[str] = Field(
        description="List of behavioral questions generated."
    )
    technical_questions: List[str] = Field(
        description="List of technical questions generated."
    )


class InterviewAnswersGeneratorSchema(BaseModel):
    answers_general_questions: List[str] = Field(
        description="List of answers to the general questions generated."
    )
    answers_behavioral_questions: List[str] = Field(
        description="List of answers to the behavioral questions generated."
    )
    answers_technical_questions: List[str] = Field(
        description="List of answers to the technical questions generated."
    )


class InterviewAdditionalResourcesGeneratorSchema(BaseModel):
    additional_resources: List[str] = Field(
        description="List of additional resources that can be used to prepare for the interview."
    )
