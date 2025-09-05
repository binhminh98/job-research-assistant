"""
Module to specify base abstract langchain chain for job research assistant app.
"""

from abc import ABC, abstractmethod
from typing import Any

from config import OPENAI_API_KEY
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSerializable
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


class BaseChain(ABC):
    @abstractmethod
    def __init__(self, model_name: str, temperature: float):
        self.chat_model = ChatOpenAI(
            model=model_name,
            api_key=SecretStr(OPENAI_API_KEY or ""),
            temperature=temperature,
        )
        self.response_schema = self._construct_response_schema()
        self.prompt = self._construct_prompt()
        self.chain = self._construct_chain()

    @abstractmethod
    def _construct_response_schema(self) -> Any:
        pass

    @abstractmethod
    def _construct_prompt(self) -> PromptTemplate:
        pass

    @abstractmethod
    def _construct_chain(self) -> RunnableSerializable:
        pass

    def run_chain(self, input_data: dict) -> Any:
        filtered_input_data = self._filter_input_data(input_data)
        return self.chain.invoke(filtered_input_data).model_dump()

    def _filter_input_data(self, input_data: dict) -> dict:
        """Filter input_data to only include variables expected by the prompt"""
        expected_variables = set(self.prompt.input_variables)

        # Only include expected variables
        filtered_data = {
            key: value
            for key, value in input_data.items()
            if key in expected_variables
        }

        # Ensure all required variables are present
        missing_variables = expected_variables - set(filtered_data.keys())
        if missing_variables:
            raise ValueError(
                f"Missing required input variables: {list(missing_variables)}"
            )

        return filtered_data
