from datetime import UTC, date, datetime, timedelta
from enum import StrEnum
from typing import Annotated

from pydantic import AwareDatetime, BeforeValidator
from pydantic_core.core_schema import ValidationInfo

YouTrackDate = Annotated[
    date,
    BeforeValidator(
        lambda d: (datetime.fromtimestamp(d / 1000, UTC) - timedelta(hours=12)) if isinstance(d, int) else d,
    ),
]


def validate_youtrack_datetime(value, info: ValidationInfo):
    if "project_custom_field" not in info.data:
        raise RuntimeError("validate_youtrack_datetime can only be used with models having project_custom_field")
    if (
        (project_custom_field := info.data["project_custom_field"])
        and (project_custom_field.field.field_type.id == "date and time")
        and value is not None
    ):
        if isinstance(value, datetime):
            return value

        if not isinstance(value, int):
            raise ValueError("'date and time' field must be an integer")

        return datetime.fromtimestamp(value / 1000, UTC)

    return value


YouTrackDateTime = Annotated[AwareDatetime, BeforeValidator(validate_youtrack_datetime)]


class IssueLinkDirection(StrEnum):
    OUTWARD = "s"
    INWARD = "t"
    BOTH = ""
