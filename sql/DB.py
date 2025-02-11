from model.result import Result
from django.db import connection


def call_sp(sp_name: str, params, columns=None) -> Result:
    if columns is None:
        columns = [Result.MESSAGE, Result.RESPONSE]
    else:
        columns = [Result.MESSAGE, Result.RESPONSE] + columns

    try:
        with connection.cursor() as cursor:
            cursor.callproc(sp_name, params)
            result = cursor.fetchall()
            return Result(result, columns)
    except Exception as ex:
        return Result.exception_result(ex)
