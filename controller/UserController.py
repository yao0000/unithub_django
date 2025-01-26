from django.views.decorators.csrf import csrf_exempt

from sql.DAL.userDAL import User
from model.json_result import json_format


@csrf_exempt
def login(request):
    """
        return:
        success or fail
        status_code
        user uid

    status_code:
        0 = Success
        -1 = Exception
        -3 = Account not found
        -4 = Incorrect password
        -5 = Blocked
        -6 = Pending Approval
    """
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        result = User.login_result(email, password)
        data = result.table.loc[0, User.GUID] if result.is_success() else None
        json = {'GUID': data}
        return json_format(result, json)


@csrf_exempt
def register(request):
    """
    return:
        success or fail
        status_code

    status_code:
        0 = Success
        -1 = Exception
        -3 = Email already exists
        -4 = Username already exists
    """
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        result = User.register_result(username, email, password)
        return json_format(result)


@csrf_exempt
# for manage page
def get_users_list(request):
    """
    return:
        success or fail
        status_code
        users object in array

    status_code:
        0 = Success
        -1 = Exception
        -3 = No data found
    """
    if request.method == "GET":
        result = User.get_users_list()
        data = []

        if result.is_success():
            data = result.table[User.USERNAME].tolist()

        return json_format(result, data)


@csrf_exempt
def update_access_right(request):
    """
    return:
        success or fail
        status_code

    status_code:
        0 = Success
        -1 = Exception
        -3 = Invalid Access
        -4 = User not found
    """
    if request.method == "POST":
        admin_guid = request.POST.get('admin_guid')
        user_guid = request.POST.get('user_guid')
        new_access_right = request.POST.get('new_access_right')
        #  1: Pending; 0: Active; Else: Block;

        result = User.update_access_right(admin_guid, user_guid, new_access_right)
        return json_format(result)


@csrf_exempt
def get_user_details(request):
    """
    waiting to dev
    return:
        success or fail
        status_code
        user details: Object

    status_code:
        0 = Success
        -1 = Exception
        -3 = No data found

    """
    if request.method == "POST":
        guid = request.POST.get('guid')
        result = User.get_user_details(guid)
        data = {}

        if result.is_success():
            temp = result.table.iloc[0]
            data = {
                User.USERNAME: temp[User.USERNAME],
                User.EMAIL: temp[User.EMAIL],
                User.ACCESS_RIGHT: temp[User.ACCESS_RIGHT],
                User.CREATED_TIME: temp[User.CREATED_TIME],
                User.GUID: temp[User.GUID],
            }

        return json_format(result, data)
