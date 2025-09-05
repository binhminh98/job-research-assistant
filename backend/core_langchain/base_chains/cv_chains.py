"""
Module to specify langchain base CV chains for job research assistant app.
"""

from core_langchain.base_chains.base_chains import BaseChain
from core_langchain.base_prompts.cv_prompts import (
    ATSKeywordsPrompt,
    CVImprovedBulletPointsPrompt,
    CVMainBulletPointsExtractionPrompt,
    CVParserPrompt,
    SkillsGapAnalysisPrompt,
)
from core_langchain.response_schemas.cv_response_schemas import (
    ATSKeywordsSchema,
    CVImprovedBulletPointsSchema,
    CVMainBulletPointsSchema,
    CVResponseSchema,
    SkillsGapSchema,
)
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSerializable
from langchain_core.output_parsers import PydanticOutputParser


class CVParserChain(BaseChain):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def _construct_response_schema(self) -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=CVResponseSchema)

    def _construct_prompt(self) -> PromptTemplate:
        return CVParserPrompt(self.response_schema).get_prompt()

    def _construct_chain(self) -> RunnableSerializable:
        return self.prompt | self.chat_model | self.response_schema


class SkillsGapAnalysisChain(BaseChain):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def _construct_response_schema(self) -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=SkillsGapSchema)

    def _construct_prompt(self) -> PromptTemplate:
        return SkillsGapAnalysisPrompt(self.response_schema).get_prompt()

    def _construct_chain(self) -> RunnableSerializable:
        return self.prompt | self.chat_model | self.response_schema


class CVMainBulletPointsExtractionChain(BaseChain):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def _construct_response_schema(self) -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=CVMainBulletPointsSchema)

    def _construct_prompt(self) -> PromptTemplate:
        return CVMainBulletPointsExtractionPrompt(
            self.response_schema
        ).get_prompt()

    def _construct_chain(self) -> RunnableSerializable:
        return self.prompt | self.chat_model | self.response_schema


class CVImprovedBulletPointsChain(BaseChain):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def _construct_response_schema(self) -> PydanticOutputParser:
        return PydanticOutputParser(
            pydantic_object=CVImprovedBulletPointsSchema
        )

    def _construct_prompt(self) -> PromptTemplate:
        return CVImprovedBulletPointsPrompt(self.response_schema).get_prompt()

    def _construct_chain(self) -> RunnableSerializable:
        return self.prompt | self.chat_model | self.response_schema


class ATSKeywordsChain(BaseChain):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def _construct_response_schema(self) -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=ATSKeywordsSchema)

    def _construct_prompt(self) -> PromptTemplate:
        return ATSKeywordsPrompt(self.response_schema).get_prompt()

    def _construct_chain(self) -> RunnableSerializable:
        return self.prompt | self.chat_model | self.response_schema


if __name__ == "__main__":
    from config import MINIO_ACCESS_KEY, MINIO_ENDPOINT, MINIO_SECRET_KEY
    from langchain_community.document_loaders.s3_file import S3FileLoader

    BUCKET_NAME = "jobsearch-original-files"

    def retrieve_raw_cv_object(docx_object_key):
        file_loader = S3FileLoader(
            bucket=BUCKET_NAME,
            key=docx_object_key,
            endpoint_url=f"http://{MINIO_ENDPOINT}",
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            use_ssl=False,
        )

        return file_loader.load()

    docx_object_key = "32c8982bff784c4b959c3231918240b2ab756ea032a5174742672bea7d82b918/MinhLai_CV_BuroHappold.docx"

    cv_chain = CVParserChain(model_name="gpt-3.5-turbo", temperature=0.3)

    input_data = {
        "raw_cv_text": retrieve_raw_cv_object(docx_object_key)[0].page_content
    }

    print(cv_chain.run_chain(input_data))
