from sql.const_value.const_sp import SP
from model.result import Result
from sql.DB import call_sp


class User:
    ID = 'ID'
    USERNAME = 'Username'
    EMAIL = 'Email'
    SALT = 'Salt'
    ROLE = 'Role'
    ACCESS_RIGHT = 'AccessRight'
    CREATED_DATE = 'CreatedDate'
    GUID = 'GUID'

    COLUMNS = [Result.MESSAGE, Result.RESPONSE, ID, USERNAME, EMAIL, SALT, ROLE, ACCESS_RIGHT, CREATED_DATE, GUID]
    LOGIN_COLUMNS = ['Message', 'Response', 'GUID']

    def __init__(self, id_no, username, email, salt, role, created_date):
        self.id = id_no
        self.username = username
        self.email = email
        self.salt = salt
        self.role = role
        self.createdDate = created_date

    @staticmethod
    def login_result(email: str, password: str) -> Result:
        params = (email, password)
        return call_sp(SP.SP_User_Login, params, User.LOGIN_COLUMNS)

    @staticmethod
    def register_result(username: str, email: str, password: str) -> Result:
        params = (username, email, password)
        return call_sp(SP.SP_User_Register, params, Result.COLUMNS)

    @staticmethod
    def get_users_list() -> Result:
        return call_sp(SP.SP_User_Get_User_List, None, User.COLUMNS)


'''
    @staticmethod
    def update_users_access_right(admin_guid: str, user_guid: str, new_status: int) -> Result:
        params = (admin_guid, user_guid, new_status)
        result = SQL().call_sp(SP.SP_User_Update_Users_Access_Right, params)
        return Result(result, Result.COLUMNS)
'''
