"""Module to create langchain chains factory for job research assistant app."""

from pathlib import Path

from core_langchain.base_chains.company_parser_chains import (
    CompanyInfoParserChain,
)
from core_langchain.base_chains.cv_chains import (
    ATSKeywordsChain,
    CVImprovedBulletPointsChain,
    CVMainBulletPointsExtractionChain,
    CVParserChain,
    SkillsGapAnalysisChain,
)
from core_langchain.base_chains.interview_chains import (
    InterviewAdditionalResourcesGeneratorChain,
    InterviewAnswersGeneratorChain,
    InterviewQuestionsGeneratorChain,
)
from core_langchain.base_chains.jd_chains import JobDescriptionParserChain
from db_connectors.postgres.postgres_client import (
    PGVectorClient,
    PostgresClient,
)
from general_utils.logging import get_logger
from langchain.schema.runnable import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableSerializable,
)
from langchain_openai import OpenAIEmbeddings
from rapidfuzz import process

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/chains_factory/chains_factory.log"),
)

stream_logger = get_logger(
    "stream_" + __name__,
)

# Initialize Postgres and PGVector clients
POSTGRES_CLIENT = PostgresClient()
EMBEDDING_FUNCTION = OpenAIEmbeddings()
PGVECTOR_JD = PGVectorClient(EMBEDDING_FUNCTION, "job_descriptions")
PGVECTOR_COMPANY_INFO = PGVectorClient(EMBEDDING_FUNCTION, "company_info")


def get_matching_strings(
    input_name: str, known_names: list[str], threshold: int = 85
):
    """
    Function to find the best matched strings (e.g some_company_name -> company_name).

    Args:
        input_name: str
        known_names: list[str]
        threshold: int

    Returns:
        list[str]
    """
    matches = process.extract(input_name, known_names, limit=None)
    return [match for match, score, _ in matches if score >= threshold]


class ChainsFactory:
    """Factory class to create langchain chains for job research assistant app."""

    _base_chain_classes = {
        "cv_parser": CVParserChain,
        "job_description_parser": JobDescriptionParserChain,
        "company_info_parser": CompanyInfoParserChain,
        "skills_gap_analizer": SkillsGapAnalysisChain,
        "cv_main_bullet_points_extractor": CVMainBulletPointsExtractionChain,
        "cv_improved_bullet_points_generator": CVImprovedBulletPointsChain,
        "ats_keywords_generator": ATSKeywordsChain,
        "interview_questions_generator": InterviewQuestionsGeneratorChain,
        "interview_answers_generator": InterviewAnswersGeneratorChain,
        "interview_additional_resources_generator": InterviewAdditionalResourcesGeneratorChain,
    }

    def __init__(self, model_name: str, temperature: float):
        self.model_name = model_name
        self.temperature = temperature
        self._chain_cache = {}

    def _get_base_chain(self, chain_type: str):
        """Lazy loading of chains with caching"""
        if (
            chain_type not in self._chain_cache
            and chain_type in self._base_chain_classes
        ):
            self._chain_cache[chain_type] = self._base_chain_classes[
                chain_type
            ](self.model_name, self.temperature)

        return self._chain_cache[chain_type].chain

    ### HELPER FUNCTIONS ###
    def _retrieve_cv_text(self, data, text_type="extracted_text"):
        cv_file_hash = data["cv_file_hash"]

        try:
            query = f"""
                    SELECT {text_type}
                    from public.cv_data cd where cd.file_hash = :cv_file_hash
                """

            result = POSTGRES_CLIENT.query_db(
                query, params={"cv_file_hash": cv_file_hash}
            )

            if result:
                extracted_cv_text = result.fetchone()[0]
            else:
                extracted_cv_text = {}

        except Exception as e:
            extracted_cv_text = {}
            file_logger.error(f"Error extracting CV text: {e}")
            stream_logger.error(f"Error extracting CV text: {e}")

        return extracted_cv_text

    def _retrieve_relevant_contexts(
        self, data, rag_collection="job_description", k=10
    ):
        job_title = data["job_title"]

        # Query to get relevant company names from the database
        company_name = data["company_name"]
        query = f"""
            SELECT DISTINCT lpe.cmetadata->>'company_name' AS company_name
            FROM langchain_pg_embedding lpe
            WHERE lpe.cmetadata->>'company_name' IS NOT NULL;
        """
        result = POSTGRES_CLIENT.query_db(query)
        known_company_names = (
            list({row[0] for row in result.fetchall()}) if result else list()
        )

        company_names = get_matching_strings(company_name, known_company_names)

        if rag_collection == "job_description":
            relevant_context = PGVECTOR_JD.similarity_search(
                query=job_title,
                metadata_filter={
                    "company_name": company_names,
                    "job_title": job_title,
                },
                k=k,
            )

        elif rag_collection == "company_values":
            relevant_context = PGVECTOR_COMPANY_INFO.similarity_search(
                query=company_name,
                metadata_filter={"company_name": company_names},
                k=k,
            )

        else:
            relevant_context = []

        # Combine retrieved context into a single string
        full_context_text = " ".join(
            [chunk.page_content for chunk in relevant_context]
        )

        return full_context_text

    ### END HELPER FUNCTIONS ###

    ### FACTORY FUNCTIONS ###

    def create_complete_cv_recommendations_chain(self) -> RunnableSerializable:
        """
        Create a complete CV recommendations chain.

        Input data:
        - cv_file_hash: str
        - company_name: str
        - job_title: str

        Output data:
        - general_recommendations: str
        - job_description_ats_skills_extracted: str
        - match_score: float
        - missing_skills: list[str]
        - matched_skills: list[str]
        - new_cv_bullet_points: list[str]
        - ats_keywords_included: list[str]
        """
        skills_gap_analizer = self._get_base_chain("skills_gap_analizer")
        cv_main_bullet_points_extractor = self._get_base_chain(
            "cv_main_bullet_points_extractor"
        )
        cv_improved_bullet_points_generator = self._get_base_chain(
            "cv_improved_bullet_points_generator"
        )
        ats_keywords_generator = self._get_base_chain("ats_keywords_generator")

        complete_cv_recommendations_chain = (
            # Step 1: Retrieve extracted CV text and job description context
            RunnablePassthrough.assign(
                extracted_cv_text=lambda data: self._retrieve_cv_text(data),
                job_description=lambda data: self._retrieve_relevant_contexts(
                    data, "job_description"
                ),
            )
            # Step 2: Generate skills gap from CV and job description
            | RunnablePassthrough.assign(
                skills_gap_result=lambda data: skills_gap_analizer.invoke(
                    {
                        "extracted_cv_text": data["extracted_cv_text"],
                        "job_description": data["job_description"],
                    }
                ).model_dump()
            )
            # Step 3: Retrieve extracted CV text
            | RunnablePassthrough.assign(
                raw_cv_text=lambda data: self._retrieve_cv_text(
                    data, "raw_text"
                ),
            )
            # Step 4: Extract main bullet points from CV
            | RunnablePassthrough.assign(
                main_bullet_points=lambda data: cv_main_bullet_points_extractor.invoke(
                    {"raw_cv_text": data["raw_cv_text"]}
                ).model_dump()[
                    "main_bullet_points"
                ]
            )
            # Step 5: Generate new CV bullet points for CV
            | RunnablePassthrough.assign(
                new_cv_bullet_points=lambda data: cv_improved_bullet_points_generator.invoke(
                    {
                        "job_description_ats_skills_extracted": data[
                            "skills_gap_result"
                        ]["job_description_ats_skills_extracted"],
                        "main_bullet_points": data["main_bullet_points"],
                    }
                ).model_dump()[
                    "new_cv_bullet_points"
                ]
            )
            # Step 6: Generate ATS keywords included in the new CV bullet points
            | RunnablePassthrough.assign(
                ats_keywords_included=lambda data: ats_keywords_generator.invoke(
                    {
                        "job_description_ats_skills_extracted": data[
                            "skills_gap_result"
                        ]["job_description_ats_skills_extracted"],
                        "new_cv_bullet_points": data["new_cv_bullet_points"],
                    }
                ).model_dump()[
                    "ats_keywords_included"
                ]
            )
            # Step 7: Return only the desired output
            | RunnableLambda(
                lambda data: {
                    "general_recommendations": data["skills_gap_result"][
                        "general_recommendations"
                    ],
                    "job_description_ats_skills_extracted": data[
                        "skills_gap_result"
                    ]["job_description_ats_skills_extracted"],
                    "match_score": data["skills_gap_result"]["match_score"],
                    "missing_skills": data["skills_gap_result"][
                        "missing_skills"
                    ],
                    "matched_skills": data["skills_gap_result"][
                        "matched_skills"
                    ],
                    "new_cv_bullet_points": data["new_cv_bullet_points"],
                    "ats_keywords_included": data["ats_keywords_included"],
                }
            )
        )

        return complete_cv_recommendations_chain

    def create_complete_interview_preparation_chain(
        self,
    ) -> RunnableSerializable:
        """
        Create a complete interview preparation chain.

        Input data:
        - company_name: str
        - job_title: str

        Output data:
        - generated_interview_questions: list[str]
        - generated_interview_answers: list[str]
        - generated_additional_resources: list[str]
        """
        interview_questions_generator = self._get_base_chain(
            "interview_questions_generator"
        )
        interview_answers_generator = self._get_base_chain(
            "interview_answers_generator"
        )
        interview_additional_resources_generator = self._get_base_chain(
            "interview_additional_resources_generator"
        )

        complete_interview_preparation_chain = (
            # Step 1: Retrieve relevant job description context and company values context
            RunnablePassthrough.assign(
                job_description=lambda data: self._retrieve_relevant_contexts(
                    data, "job_description"
                ),
                company_values=lambda data: self._retrieve_relevant_contexts(
                    data, "company_values"
                ),
            )
            # Step 2: Generate interview questions
            | RunnablePassthrough.assign(
                generated_interview_questions=lambda data: interview_questions_generator.invoke(
                    {
                        "job_description": data["job_description"],
                        "company_values": data["company_values"],
                    }
                ).model_dump()
            )
            # Step 3: Generate interview answers
            | RunnablePassthrough.assign(
                generated_interview_answers=lambda data: interview_answers_generator.invoke(
                    {
                        "generated_interview_questions": data[
                            "generated_interview_questions"
                        ]
                    }
                ).model_dump()
            )
            # Step 4: Generate additional resources
            | RunnablePassthrough.assign(
                generated_additional_resources=lambda data: interview_additional_resources_generator.invoke(
                    {
                        "generated_interview_questions": data[
                            "generated_interview_questions"
                        ]
                    }
                ).model_dump()
            )
            # Step 5: Return only the desired output
            | RunnableLambda(
                lambda data: {
                    "generated_interview_questions": data[
                        "generated_interview_questions"
                    ],
                    "generated_interview_answers": data[
                        "generated_interview_answers"
                    ],
                    "generated_additional_resources": data[
                        "generated_additional_resources"
                    ],
                }
            )
        )

        return complete_interview_preparation_chain


if __name__ == "__main__":
    chains_factory = ChainsFactory(model_name="gpt-3.5-turbo", temperature=0.3)
    # complete_cv_recommendations_chain = (
    #     chains_factory.create_complete_cv_recommendations_chain()
    # )
    complete_interview_preparation_chain = (
        chains_factory.create_complete_interview_preparation_chain()
    )
    initial_input = {
        "company_name": "Aviva",
        "job_title": "AI Specialist Developer",
        # "cv_file_hash": "32c8982bff784c4b959c3231918240b2ab756ea032a5174742672bea7d82b918",
    }

    # print(complete_cv_recommendations_chain.invoke(initial_input))
    print(complete_interview_preparation_chain.invoke(initial_input))
