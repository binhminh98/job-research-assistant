"""
Module to specify base prompts for langchain base chains.
"""

from abc import ABC, abstractmethod

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


class BasePrompt(ABC):
    @abstractmethod
    def __init__(self, response_schema: PydanticOutputParser):
        pass

    @abstractmethod
    def get_prompt(self) -> PromptTemplate:
        pass
