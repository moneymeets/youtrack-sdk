class YouTrackException(Exception):
    pass


class YouTrackNotFound(YouTrackException):
    pass


class YouTrackUnauthorized(YouTrackException):
    pass
