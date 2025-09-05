"""
Module to specify langchain base company info chains for job research assistant app.
"""

from core_langchain.base_chains.base_chains import BaseChain
from core_langchain.base_prompts.company_parser_prompts import (
    CompanyInfoParserPrompt,
)
from core_langchain.response_schemas.company_parser_response_schemas import (
    CompanyInfoSchema,
)
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSerializable


class CompanyInfoParserChain(BaseChain):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def _construct_response_schema(self) -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=CompanyInfoSchema)

    def _construct_prompt(self) -> PromptTemplate:
        return CompanyInfoParserPrompt(self.response_schema).get_prompt()

    def _construct_chain(self) -> RunnableSerializable:
        return self.prompt | self.chat_model | self.response_schema
