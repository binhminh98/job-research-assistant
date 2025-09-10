"""
Utility module to interact with the backend API.
"""

import base64
from pathlib import Path
from typing import Any, Dict

import requests
from config import BACKEND_URL
from requests.exceptions import ConnectionError, RequestException, Timeout
from utils.logging import get_logger

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/frontend/backend_api_client.log"),
)

stream_logger = get_logger(
    "stream_" + __name__,
)


class BackendApiClient:
    def __init__(self, timeout: int = 30):
        self.backend_base_url = BACKEND_URL
        self.timeout = timeout

    def _get_session(self):
        return requests.Session()

    def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request to backend API."""
        url = f"{self.backend_base_url}{endpoint}"

        try:
            with self._get_session() as session:
                response = session.request(
                    method=method, url=url, timeout=self.timeout, **kwargs
                )

                if response.status_code == 200:
                    return {
                        "success": True,
                        "data": response.json(),
                        "status_code": response.status_code,
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "status_code": response.status_code,
                    }

        except ConnectionError:
            return {
                "success": False,
                "error": "Could not connect to backend server",
                "status_code": 0,
            }
        except Timeout:
            return {
                "success": False,
                "error": "Request timed out",
                "status_code": 0,
            }
        except RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "status_code": 0,
            }

    def upload_file(self, username: str, file_content: str, filename: str):
        try:
            # Parse the base64 content
            if "," in file_content:
                _, base64_content = file_content.split(",", 1)
            else:
                base64_content = file_content

            file_bytes = base64.b64decode(base64_content)

            # Prepare multipart data
            files = {
                "file": (
                    filename,
                    file_bytes,
                    "application/octet-stream",
                )
            }
            params = {"username": username}

            url = f"{self.backend_base_url}/upload_file/"

            with self._get_session() as session:
                response = session.post(
                    url=url, files=files, params=params, timeout=self.timeout
                )

                if response.status_code == 200:
                    return {
                        "success": True,
                        "data": response.json(),
                        "status_code": response.status_code,
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "status_code": response.status_code,
                    }

        except Exception as e:
            file_logger.error(f"Upload failed: {str(e)}")
            stream_logger.error(f"Upload failed: {str(e)}")
            return {
                "success": False,
                "error": f"Upload failed: {str(e)}",
                "status_code": 0,
            }

    def extract_jd_urls(self, jd_urls: list):
        return self._make_request(
            "POST", "/analyze/extract_jd_urls", json=jd_urls
        )

    def extract_company_urls(self, company_urls: list):
        return self._make_request(
            "POST", "/analyze/extract_company_urls", json=company_urls
        )

    def analyze_cv(
        self,
        username: str,
        cv_object_key: str,
        company_name: str,
        job_title: str,
    ):
        return self._make_request(
            "POST",
            "/analyze/analyze_cv",
            params={
                "username": username,
                "cv_object_key": cv_object_key,
                "company_name": company_name,
                "job_title": job_title,
            },
        )

    def get_cv_analysis_jobs(self, username: str):
        return self._make_request(
            "GET",
            f"/analyze/get_cv_analysis_jobs",
            params={"username": username},
        )

    def get_cv_analysis_job_by_id(self, job_id: int):
        return self._make_request(
            "GET",
            f"/analyze/get_cv_analysis_job_by_id",
            params={"job_id": job_id},
        )

    def interview_prep(self, company_name: str, job_title: str):
        return self._make_request(
            "POST",
            "/interview_prep",
            params={"company_name": company_name, "job_title": job_title},
        )

    def get_users(self):
        return self._make_request("GET", "/users")

    def create_user(self, username: str, email: str, password: str):
        return self._make_request(
            "POST",
            "/users/create_user",
            json={
                "username": username,
                "email": email,
                "password": password,
            },
        )

    def get_user_by_username(self, username: str):
        return self._make_request("GET", f"/users/get_user/{username}")

    def get_user_by_email(self, email: str):
        return self._make_request("GET", f"/users/get_user/{email}")

    def get_cv_data_by_username(self, username: str):
        return self._make_request(
            "GET", f"/cv_data/get_cv_data_by_username/{username}"
        )

    def get_cv_data_by_file_hash(self, file_hash: str):
        return self._make_request(
            "GET", f"/cv_data/get_cv_data_by_file_hash/{file_hash}"
        )

    def get_company_names(self, company_name: str | None = None):
        return self._make_request(
            "GET",
            f"/embeddings_data/get_company_names",
            json={"company_name": company_name},
        )

    def get_job_titles(self, company_name: str | None = None):
        return self._make_request(
            "GET",
            f"/embeddings_data/get_job_titles",
            json={"company_name": company_name},
        )

    def health_check(self):
        return self._make_request("GET", "/health")


if __name__ == "__main__":
    backend_api_client = BackendApiClient()
    print(backend_api_client.create_user("test", "test@test.com", "test"))
