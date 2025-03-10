from model.json_result import json_format
from model.result import Result
from sql.DAL.DraftDAL import Draft
from sql.DB import call_sp
from sql.const_value.const_sp import SP


class Reservation:
    ID = 'ID'
    AUTHOR_GUID = 'AuthorGUID'
    STATUS = 'Status'
    CREATED_TIME = 'CreatedTime'
    CLIENT_DATA_GUID = 'DraftGUID'

    TABLE_COLUMNS = [AUTHOR_GUID, STATUS, Draft.CREATED_TIME, CLIENT_DATA_GUID]
    RESERVATION_LIST_COLUMNS = [Draft.TITLE, Draft.FULL_NAME, STATUS, CREATED_TIME]

    @staticmethod
    def get_reservation_list(author_guid: str):
        params = (author_guid, )
        result = call_sp(SP.SP_Reservation_Get_List, params, Reservation.RESERVATION_LIST_COLUMNS)
        data = []

        if result.is_success():
            data = result.table[Reservation.RESERVATION_LIST_COLUMNS].to_dict(orient='records')

        return json_format(result, data)

    @staticmethod
    def create_reservation(author_guid: str, status: str, client_data_guid: str):
        params = (author_guid, status, client_data_guid)
        result = call_sp(SP.SP_Reservation_Create_Data, params)
        return json_format(result)
