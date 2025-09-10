"""
Embeddings data CRUD endpoints for the Job Research Assistant backend.
"""

from api_utils.embeddings_data_crud_utils import EmbeddingsDataCrudApiUtils


class EmbeddingsDataCrudServices:
    @staticmethod
    def get_company_names(company_name: str | None) -> dict | None:
        return EmbeddingsDataCrudApiUtils.get_company_names(company_name)

    @staticmethod
    def get_job_titles(
        company_name: str | None,
    ) -> dict | None:
        return EmbeddingsDataCrudApiUtils.get_job_titles(company_name)
