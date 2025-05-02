from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

from sql.DAL.userDAL import User


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
        password = make_password(password)

        return User.register_result(username, email, password)


@csrf_exempt
def get_users_list(request):
    """
    Handle user listing (with pagination & search).
    """
    if request.method == "GET":
        page_start = request.GET.get('page_start', 0)
        page_size = request.GET.get('page_size', 10)
        search_term = request.GET.get('search_term', '')

        return User.get_users_list(page_start, page_size, search_term)


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
    
    Access right:   
        0: Pending 
        1: Active 
        Else: Block
    """
    if request.method == "POST":
        admin_guid = request.POST.get('admin_guid')
        user_guid = request.POST.get('user_guid')
        new_access_right = request.POST.get('new_access_right')
        # 

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


@csrf_exempt
def delete_user(request):
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
        return User.delete_result(admin_guid, user_guid)
