"""
Module to specify langchain base interview chains for job research assistant app.
"""

from core_langchain.base_chains.base_chains import BaseChain
from core_langchain.base_prompts.interview_prompts import (
    InterviewAdditionalResourcesGeneratorPrompt,
    InterviewAnswersGeneratorPrompt,
    InterviewQuestionsGeneratorPrompt,
)
from core_langchain.response_schemas.interview_response_schemas import (
    InterviewAdditionalResourcesGeneratorSchema,
    InterviewAnswersGeneratorSchema,
    InterviewQuestionsGeneratorSchema,
)
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSerializable
from langchain_core.output_parsers import PydanticOutputParser


class InterviewQuestionsGeneratorChain(BaseChain):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def _construct_response_schema(self) -> PydanticOutputParser:
        return PydanticOutputParser(
            pydantic_object=InterviewQuestionsGeneratorSchema
        )

    def _construct_prompt(self) -> PromptTemplate:
        return InterviewQuestionsGeneratorPrompt(
            self.response_schema
        ).get_prompt()

    def _construct_chain(self) -> RunnableSerializable:
        return self.prompt | self.chat_model | self.response_schema


class InterviewAnswersGeneratorChain(BaseChain):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def _construct_response_schema(self) -> PydanticOutputParser:
        return PydanticOutputParser(
            pydantic_object=InterviewAnswersGeneratorSchema
        )

    def _construct_prompt(self) -> PromptTemplate:
        return InterviewAnswersGeneratorPrompt(
            self.response_schema
        ).get_prompt()

    def _construct_chain(self) -> RunnableSerializable:
        return self.prompt | self.chat_model | self.response_schema


class InterviewAdditionalResourcesGeneratorChain(BaseChain):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def _construct_response_schema(self) -> PydanticOutputParser:
        return PydanticOutputParser(
            pydantic_object=InterviewAdditionalResourcesGeneratorSchema
        )

    def _construct_prompt(self) -> PromptTemplate:
        return InterviewAdditionalResourcesGeneratorPrompt(
            self.response_schema
        ).get_prompt()

    def _construct_chain(self) -> RunnableSerializable:
        return self.prompt | self.chat_model | self.response_schema
