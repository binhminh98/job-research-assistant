"""
Module to specify analyze services for job research assistant app.
"""

from api_utils.analyze_api_utils import AnalyzeApiUtils


class AnalyzeServices:

    @staticmethod
    def extract_jd_urls(jd_urls, url_type):
        return AnalyzeApiUtils.extract_urls(jd_urls, url_type)

    @staticmethod
    def extract_company_urls(company_urls, url_type):
        return AnalyzeApiUtils.extract_urls(company_urls, url_type)

    @staticmethod
    def analyze(username, cv_object_key, company_name, job_title):
        return AnalyzeApiUtils.analyze(
            username, cv_object_key, company_name, job_title
        )

    @staticmethod
    def get_cv_analysis_jobs(username):
        return AnalyzeApiUtils.get_cv_analysis_jobs(username)

    @staticmethod
    def get_cv_analysis_job_by_id(job_id):
        return AnalyzeApiUtils.get_cv_analysis_job_by_id(job_id)
