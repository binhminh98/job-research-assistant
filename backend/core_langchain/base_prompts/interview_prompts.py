"""
Module to specify base prompts for langchain interview chains.
"""

from core_langchain.base_prompts.base_prompts import BasePrompt
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


class InterviewQuestionsGeneratorPrompt(BasePrompt):
    def __init__(self, response_schema: PydanticOutputParser):
        self.response_schema = response_schema

    def get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template=(
                "You are an expert interview question generator.\n\n"
                "Job Description:\n{job_description}\n\n"
                "Company Values and Culture:\n{company_values}\n\n"
                "Based on the job description and company values, generate a set of 10 interview questions for each category.\n"
                "Include questions in the following categories:\n"
                "- Technical Questions\n"
                "- Behavioral Questions\n"
                "- General Questions\n\n"
                "Please use this format:\n\n"
                "{format_instructions}\n\n"
            ),
            input_variables=[
                "job_description",
                "company_values",
            ],
            partial_variables={
                "format_instructions": self.response_schema.get_format_instructions()
            },
        )


class InterviewAnswersGeneratorPrompt(BasePrompt):
    def __init__(self, response_schema: PydanticOutputParser):
        self.response_schema = response_schema

    def get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template=(
                "You are an expert interview question answer generator.\n\n"
                "Interview questions:\n{generated_interview_questions}\n\n"
                "Please help me to generate example answers for these interview questions using the STARR method (situation - tasks - actions - results - reflections). The answers should not exceed 6 sentences, keep the answers sharp and precise, professional:\n"
                "Include answers in the following categories:\n"
                "- Technical Answers\n"
                "- Behavioral Answers\n"
                "- General Answers\n\n"
                "Please use this format:\n\n"
                "{format_instructions}\n\n"
            ),
            input_variables=[
                "generated_interview_questions",
            ],
            partial_variables={
                "format_instructions": self.response_schema.get_format_instructions()
            },
        )


class InterviewAdditionalResourcesGeneratorPrompt(BasePrompt):
    def __init__(self, response_schema: PydanticOutputParser):
        self.response_schema = response_schema

    def get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template=(
                "You are an expert interview question answer generator.\n\n"
                "Please help me to find additional resources to prepare for these interview questions:\n"
                "Interview questions:\n{generated_interview_questions}\n\n"
                "Include additional resources, 4 in each category with links, in the following categories:\n"
                "- Technical Resources\n"
                "- Behavioral Resources\n"
                "- General Resources\n\n"
                "Please use this format:\n\n"
                "{format_instructions}\n\n"
            ),
            input_variables=[
                "generated_interview_questions",
            ],
            partial_variables={
                "format_instructions": self.response_schema.get_format_instructions()
            },
        )
