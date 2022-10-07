from pydantic.errors import PydanticValueError


class YouTrackException(Exception):
    pass


class YouTrackNotFound(YouTrackException):
    pass


class YouTrackUnauthorized(YouTrackException):
    pass


class StrictIntError(PydanticValueError):
    msg_template = "value is not a valid integer"


class IncompatibleFieldTypeError(PydanticValueError):
    msg_template = "incompatible field type"
