"""
Module to specify general utils for job research assistant app.
"""

from datetime import datetime
from decimal import Decimal

from rapidfuzz import process


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


def serialize_for_json(obj) -> dict | list | str | int | float | bool | None:
    """Convert objects to JSON-serializable format."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: serialize_for_json(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [serialize_for_json(item) for item in obj]
    elif hasattr(obj, "_asdict"):
        return serialize_for_json(obj._asdict())
    else:
        return obj
