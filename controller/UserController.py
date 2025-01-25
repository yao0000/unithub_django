from django.views.decorators.csrf import csrf_exempt

from sql.DAL.userDAL import User
from model.json_result import json_format


@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        result = User.login_result(email, password)
        data = result.table.loc[0, User.GUID] if result.is_success() else None
        json = {'GUID': data}
        return json_format(result, json)


@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        result = User.register_result(username, email, password)
        return json_format(result)


@csrf_exempt
# for manage page
def get_users_summary(request):
    if request.method == "GET":
        result = User.get_users_list()
        data = []
        if result.is_success():
            data = result.table[User.USERNAME].tolist()

        return json_format(result, data)
