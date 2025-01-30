class LoginStatus:
    SUCCESS = 0
    EXCEPTION = -1
    UNKNOWN = -2
    ACCOUNT_NOT_FOUND = -3
    INCORRECT_PASSWORD = -4
    BLOCKED = -5
    PENDING = -6


class RegisterStatus:
    SUCCESS = 0
    EXCEPTION = -1
    EMAIL_EXISTS = -3


class GetUserListStatus:
    SUCCESS = 0
    EXCEPTION = -1
    NO_DATA = -3


class UpdateAccessRightStatus:
    SUCCESS = 0
    Exception = -1
    INVALID_ACCESS = -3
    USER_NOT_FOUND = -4

    class AccessRight:
        ACTIVE = 1
        PENDING = 0
        BLOCK = -1


