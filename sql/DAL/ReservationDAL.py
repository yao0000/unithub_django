from model.result import Result
from sql.DB import call_sp
from sql.const_value.const_sp import SP


class Reservation:
    ID = 'ID'
    AUTHOR_GUID = 'AuthorGUID'
    STATUS = 'Status'
    CREATED_TIME = 'CreatedTime'
    CLIENT_DATA_GUID = 'ClientDataGUID'

    TABLE_COLUMNS = [Result.MESSAGE, Result.RESPONSE,
                     ID, AUTHOR_GUID, STATUS, CREATED_TIME, CLIENT_DATA_GUID]

    @staticmethod
    def get_reservation_list(author_guid: str):
        mode = 'SUMMARY'
        params = (mode, author_guid)
        call_sp(SP.SP_Reservation_Get_Summary, params, None)
