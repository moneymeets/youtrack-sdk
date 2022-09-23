from datetime import datetime

from pydantic.datetime_parse import from_unix_seconds
from pydantic.errors import PydanticValueError


class StrictIntError(PydanticValueError):
    msg_template = "value is not a valid integer"


class IncompatibleFieldTypeError(PydanticValueError):
    msg_template = "incompatible field type"


class DateTime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, values):
        if (project_custom_field := values.get("project_custom_field")) and (
            project_custom_field.field.field_type.id != "date and time"
        ):
            raise IncompatibleFieldTypeError

        if isinstance(value, datetime):
            return value

        if not isinstance(value, int):
            raise StrictIntError

        return from_unix_seconds(value)
