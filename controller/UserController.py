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

        return User.login_result(email, password)


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

        return User.register_result(username, email, password)


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
        return User.get_users_list()


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

        return User.update_access_right(admin_guid, user_guid, new_access_right)


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
        return User.get_user_details(guid)
