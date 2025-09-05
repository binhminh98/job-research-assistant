"""Module to specify base prompts for langchain CV chains."""

from core_langchain.base_prompts.base_prompts import BasePrompt
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


class CVParserPrompt(BasePrompt):
    def __init__(self, response_schema: PydanticOutputParser):
        self.response_schema = response_schema

    def get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template=(
                "You are a CV parser. Extract information from the CV text into JSON.\n\n"
                "{format_instructions}\n\nCV TEXT:\n{raw_cv_text}"
            ),
            input_variables=["raw_cv_text"],
            partial_variables={
                "format_instructions": self.response_schema.get_format_instructions()
            },
        )


class SkillsGapAnalysisPrompt(BasePrompt):
    def __init__(self, response_schema: PydanticOutputParser):
        self.response_schema = response_schema

    def get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template=(
                "You are an expert in comparing CV text with job requirements.\n\n"
                "Compare CV text with job requirements:\n\n"
                "{format_instructions}\n\n"
                "CV text:\n{extracted_cv_text}\n\n"
                "Job description:\n{job_description}"
            ),
            input_variables=["extracted_cv_text", "job_description"],
            partial_variables={
                "format_instructions": self.response_schema.get_format_instructions()
            },
        )


class CVMainBulletPointsExtractionPrompt(BasePrompt):
    def __init__(self, response_schema: PydanticOutputParser):
        self.response_schema = response_schema

    def get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template=(
                "You are a helpful document parser assistant.\n\n"
                "Helps me to extract all CV bullet points from original text, please don't change any wordings. Skip the skills section.\n\n"
                "Please use this format: \n\n"
                "{format_instructions}\n\n"
                "CV text:\n{raw_cv_text}"
            ),
            input_variables=["raw_cv_text"],
            partial_variables={
                "format_instructions": self.response_schema.get_format_instructions()
            },
        )


class CVImprovedBulletPointsPrompt(BasePrompt):
    def __init__(self, response_schema: PydanticOutputParser):
        self.response_schema = response_schema

    def get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template=(
                "You are an expert job advisor specializing in resume screening and cover letter advice.\n\n"
                "ATS keywords extracted:\n{job_description_ats_skills_extracted}\n\n"
                "Please transform the bullet points using this format: Accomplished [X] as measured by [Y], by doing [Z]. Each should be a maximum of 2 sentences. Include as many ATS keywords provided above as possible in a natural way, avoiding repetitive sentence structures:\n\n"
                "CV main bullet points:\n{main_bullet_points}\n\n"
                "Please use this format:\n\n"
                "{format_instructions}\n\n"
            ),
            input_variables=[
                "job_description_ats_skills_extracted",
                "main_bullet_points",
            ],
            partial_variables={
                "format_instructions": self.response_schema.get_format_instructions()
            },
        )


class ATSKeywordsPrompt(BasePrompt):
    def __init__(self, response_schema: PydanticOutputParser):
        self.response_schema = response_schema

    def get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template=(
                "You are a expert CV scanner.\n\n"
                "ATS keywords:\n{job_description_ats_skills_extracted}\n\n"
                "Please scan the new CV bullet points and give me a list of all ATS keywords included in the new CV bullet points, only include keywords that are present in the list provided above:\n\n"
                "New CV bullet points:\n{new_cv_bullet_points}\n\n"
                "Please use this format: \n\n"
                "{format_instructions}\n\n"
            ),
            input_variables=[
                "job_description_ats_skills_extracted",
                "new_cv_bullet_points",
            ],
            partial_variables={
                "format_instructions": self.response_schema.get_format_instructions()
            },
        )
