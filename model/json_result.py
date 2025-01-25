from django.http import JsonResponse
from model.result import Result


def json_format(result: Result, data=None) -> JsonResponse:
    return JsonResponse({
        'message': result.msg,
        'status_code': result.status_code,
        'data': data
    })


def exception_format(exception: Exception) -> JsonResponse:
    return JsonResponse({
        'message': exception,
        'status_code': -1
    })
