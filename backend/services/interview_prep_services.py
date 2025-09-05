"""
Module to specify services for the endpoints for interviews for job research assistant app.
"""

from api_utils.interviews_prep_api_utils import InterviewsPrepApiUtils


class InterviewPrepServices:
    @staticmethod
    def generate_interview_preparation_materials(company_name, job_title):
        return InterviewsPrepApiUtils.generate_interview_preparation_materials(
            company_name, job_title
        )
