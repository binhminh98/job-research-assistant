"""
Module to specify backend logic for the services for analyze API.
"""

import requests
from core_langchain.base_chains.company_parser_chains import (
    CompanyInfoParserChain,
)
from core_langchain.base_chains.jd_chains import JobDescriptionParserChain
from core_langchain.factory.chains_factory import ChainsFactory
from db_connectors.postgres.postgres_client import (
    PGVectorClient,
    PostgresClient,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings

EMBEDDING_FUNCTION = OpenAIEmbeddings()
POSTGRES_CLIENT = PostgresClient()
PGVECTOR_JD = PGVectorClient(EMBEDDING_FUNCTION, "job_descriptions")
PGVECTOR_COMPANY_INFO = PGVectorClient(EMBEDDING_FUNCTION, "company_info")


def filter_accessible_urls(urls):
    accessible_urls = [
        url for url in urls if requests.get(url).status_code == 200
    ]

    non_accessible_urls = [
        url for url in urls if requests.get(url).status_code != 200
    ]

    return accessible_urls, non_accessible_urls


def get_existing_urls():
    query = """
        SELECT DISTINCT jsonb_array_elements_text(lpe.cmetadata->'urls') as url
        FROM langchain_pg_embedding lpe
    """
    result = POSTGRES_CLIENT.query_db(query)
    existing_urls = {row[0] for row in result.fetchall()} if result else set()

    return existing_urls


def split_text_into_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    return chunks


def save_embeddings_to_database(
    result: dict, urls: list, text_chunks: list, url_type
):
    if url_type == "jd":
        PGVECTOR_JD.add_texts(
            text_chunks,
            metadatas=[
                {
                    "company_name": result["company_name"],
                    "job_title": result["job_title"],
                    "job_description": result["job_description"],
                    "urls": urls,
                }
            ]
            * len(text_chunks),
        )
    elif url_type == "company":
        PGVECTOR_COMPANY_INFO.add_texts(
            text_chunks,
            metadatas=[
                {
                    "company_name": result["company_name"],
                    "urls": urls,
                }
            ]
            * len(text_chunks),
        )


class AnalyzeApiUtils:

    @staticmethod
    def extract_urls(jd_urls, url_type):
        unique_urls = set(jd_urls)

        # Existing URLs
        existing_urls = get_existing_urls()

        # New URLs
        new_urls = unique_urls - existing_urls

        if new_urls:
            accessible_urls, non_accessible_urls = filter_accessible_urls(
                new_urls
            )

            loader = WebBaseLoader(web_paths=accessible_urls)

            combined_text_from_urls = "".join(
                [doc.page_content for doc in loader.load()]
            )

            # Run chains and save embeddings to database
            if url_type == "jd":
                jd_chain = JobDescriptionParserChain(
                    model_name="gpt-3.5-turbo", temperature=0.3
                )

                chain_result = jd_chain.run_chain(
                    {
                        "job_description": combined_text_from_urls,
                    }
                )

                jd_chunks = split_text_into_chunks(
                    chain_result["job_description"]
                )

                save_embeddings_to_database(
                    chain_result, accessible_urls, jd_chunks, "jd"
                )

            elif url_type == "company":
                company_info_chain = CompanyInfoParserChain(
                    model_name="gpt-3.5-turbo", temperature=0.3
                )

                chain_result = company_info_chain.run_chain(
                    {
                        "raw_company_website_text": combined_text_from_urls,
                    }
                )

                company_info_chunks = split_text_into_chunks(
                    chain_result["summarized_company_values"]
                )

                save_embeddings_to_database(
                    chain_result,
                    accessible_urls,
                    company_info_chunks,
                    "company",
                )

            else:
                raise ValueError("Invalid URL type!")

            return {
                "company_name": chain_result["company_name"],
                "job_title": (
                    chain_result["job_title"] if url_type == "jd" else None
                ),
                "accessible_urls": accessible_urls,
                "non_accessible_urls": non_accessible_urls,
                "message": "URLs extracted, and embeddings saved to database successfully!",
            }

        else:
            return {"message": "No new URLs to extract!"}

    @staticmethod
    def analyze(cv_object_key, company_name, job_title):
        cv_file_hash = cv_object_key.split("/")[0]

        chains_factory = ChainsFactory(
            model_name="gpt-3.5-turbo", temperature=0.3
        )

        complete_cv_recommendations_chain = (
            chains_factory.create_complete_cv_recommendations_chain()
        )

        input_data = {
            "cv_file_hash": cv_file_hash,
            "company_name": company_name,
            "job_title": job_title,
        }

        try:
            complete_cv_recommendations_result = (
                complete_cv_recommendations_chain.invoke(input_data)
            )
        except Exception as e:
            return {"message": "Error generating CV recommendations!"}

        return {
            "message": "CV recommendations generated successfully!",
            "result": complete_cv_recommendations_result,
        }
