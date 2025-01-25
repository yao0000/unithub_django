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
    UNKNOWN = -2
    EMAIL_EXISTS = -3
    USERNAME_EXISTS = -4


class GetUserListStatus:
    SUCCESS = 0
    EXCEPTION = -1
    UNKNOWN = -2
    NO_DATA = -3


class AccessRight:
    ACTIVE = 1
    PENDING = 0
    BLOCK = -1


