from pydantic import ValidationError

from src.config import settings


def validate_response_schema(data: dict | list, schema, many: bool = False):
    if isinstance(data, dict):
        try:
            schema(**data)
            return True
        except ValidationError:
            return False
    if many and isinstance(data, list):
        try:
            [schema(**row) for row in data]
            return True
        except ValidationError:
            return False
    return False


def validate_pagination(
    data: dict,
    schema,
    fixture_length: int,
    limit: int = settings.PAGINATION_SIZE,
    offset: int = 0,
):
    count: int = data["count"]
    results: list = data["results"]
    results_count = len(results)

    expected_on_page = count - offset
    expected_on_page = expected_on_page if expected_on_page >= 0 else 0

    fixture_is_valid = fixture_length <= count
    count_is_valid = count >= results_count
    limit_is_valid = results_count <= limit
    offset_is_valid = results_count == min(expected_on_page, limit)
    schema_is_valid = validate_response_schema(results, schema, many=True)
    return (
        fixture_is_valid
        and count_is_valid
        and limit_is_valid
        and offset_is_valid
        and schema_is_valid
    )
