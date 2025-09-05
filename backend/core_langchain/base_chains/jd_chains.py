"""
Module to specify langchain base JD chains for job research assistant app.
"""

from core_langchain.base_chains.base_chains import BaseChain
from core_langchain.base_prompts.jd_prompts import JobDescriptionParserPrompt
from core_langchain.response_schemas.jd_response_schemas import (
    JobDescriptionSchema,
)
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSerializable
from langchain_core.output_parsers import PydanticOutputParser


class JobDescriptionParserChain(BaseChain):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def _construct_response_schema(self) -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=JobDescriptionSchema)

    def _construct_prompt(self) -> PromptTemplate:
        return JobDescriptionParserPrompt(self.response_schema).get_prompt()

    def _construct_chain(self) -> RunnableSerializable:
        return self.prompt | self.chat_model | self.response_schema
