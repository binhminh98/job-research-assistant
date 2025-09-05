"""
Module to specify base prompts for langchain JD chains.
"""

from core_langchain.base_prompts.base_prompts import BasePrompt
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


class JobDescriptionParserPrompt(BasePrompt):
    def __init__(self, response_schema: PydanticOutputParser):
        self.response_schema = response_schema

    def get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template=(
                "You are an assistant that extracts clean job posting details from messy scraped HTML text.\n\n"
                "Extract and clean this job posting into a clean format. Remove 'apply now', 'similar vacancies', or navigation junk.\n\n"
                "{format_instructions} \n\n Job description:\n{job_description}"
            ),
            input_variables=["job_description"],
            partial_variables={
                "format_instructions": self.response_schema.get_format_instructions()
            },
        )
