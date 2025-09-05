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
    def analyze(cv_object_key, company_name, job_title):
        return AnalyzeApiUtils.analyze(cv_object_key, company_name, job_title)
