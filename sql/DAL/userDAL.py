from django.contrib.auth.hashers import check_password

from model.json_result import json_format
from sql.const_value.const_sp import SP
from model.result import Result
from sql.DB import call_sp


class User:
    ID = 'ID'
    USERNAME = 'Username'
    EMAIL = 'Email'
    ROLE = 'Role'
    PASSWORD = 'HashedPwd'
    ACCESS_RIGHT = 'AccessRight'
    CREATED_TIME = 'CreatedTime'
    GUID = 'GUID'

    TABLE_COLUMNS = [ID, USERNAME, EMAIL, ROLE, ACCESS_RIGHT, CREATED_TIME, GUID]
    LOGIN_COLUMNS = [PASSWORD, GUID]
    MANAGE_COLUMNS = [GUID, USERNAME, ACCESS_RIGHT, EMAIL]

    def __init__(self, id_no, username, email, role, created_date):
        self.id = id_no
        self.username = username
        self.email = email
        self.role = role
        self.createdDate = created_date

    @staticmethod
    def login_result(email: str, password: str):
        data = []
        params = (email, )
        result = call_sp(SP.SP_User_Login, params, User.LOGIN_COLUMNS)
        print(result)

        if result.status_code == 0:
            userData = result.table.iloc[0]
            isSuccess = check_password(password, userData[User.PASSWORD])
            data = {User.GUID: userData[User.GUID]}

            result.table.HashedPwd = ''
            if isSuccess == True: 
                result.msg = 'Login Successfully'
            else:
                result.msg = 'Invalid Password'
                result.status_code = -4

        return json_format(result, data)

    @staticmethod
    def register_result(username: str, email: str, password: str):
        params = (username, email, password)
        result = call_sp(SP.SP_User_Register, params)
        return json_format(result)

    @staticmethod
    def get_users_list(page_start: int, page_size: int, search_term: str):
        """
        Fetch users list with pagination and search term.
        """
        params = (page_start, page_size, search_term)
        result = call_sp(SP.SP_User_Get_List, params, User.MANAGE_COLUMNS)

        data = []
        if result.is_success() and not result.table.empty:
            data = result.table[User.MANAGE_COLUMNS].to_dict(orient='records')

        return json_format(result, data)

    @staticmethod
    def update_access_right(admin_guid: str, user_guid: str, new_status: str):
        try:
            new_status = int(new_status)
        except ValueError:
            raise ValueError("Invalid new_status value. It must be a number.")

        params = (admin_guid, user_guid, new_status)
        result = call_sp(SP.SP_User_Update_Access_Right, params)
        return json_format(result)

    @staticmethod
    def get_user_details(guid: str):
        result = call_sp(SP.SP_User_Get_Details, (guid,), User.TABLE_COLUMNS)
        data = []

        if result.is_success() and not result.table.empty:
            data = result.table[User.TABLE_COLUMNS].to_dict(orient='records')[0]

        return json_format(result, data)

    @staticmethod
    def delete_result(admin_guid: str, deleting_user_guid: str):
        params = (admin_guid, deleting_user_guid)
        result = call_sp(SP.SP_User_Delete, params)
        return json_format(result)

