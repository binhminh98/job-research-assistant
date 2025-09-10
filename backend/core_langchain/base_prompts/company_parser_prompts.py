"""
Module to specify base prompts for langchain company parser chains.
"""

from core_langchain.base_prompts.base_prompts import BasePrompt
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


class CompanyInfoParserPrompt(BasePrompt):
    def __init__(self, response_schema: PydanticOutputParser):
        self.response_schema = response_schema

    def get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template="""
                You are a HTML text cleaner. Clean the following text by:
                - Removing excess newlines, spaces, and HTML artifacts
                - Standardizing formatting
                - Keeping the meaningful content\n\n

                Then summarize the following company values and culture text concisely in 30-35 bullet points:\n\n
                {raw_company_website_text}

                Then please put all the summarized bullet points into the summarized_company_values field as a single string with bullet points like:
                - First value
                - Second value
                - Third value\n\n
                Please use this format: \n\n{format_instructions}\n\n
            """,
            input_variables=["raw_company_website_text"],
            partial_variables={
                "format_instructions": self.response_schema.get_format_instructions()
            },
        )
