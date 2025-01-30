from model.result import Result
from sql.DB import call_sp


class Reservation:
    ID = 'ID'
    AUTHOR_GUID = 'AuthorGUID'
    STATUS = 'Status'
    CREATED_TIME = 'CreatedTime'
    CLIENT_DATA_GUID = 'ClientDataGUID'

    TABLE_COLUMNS = [Result.MESSAGE, Result.RESPONSE, ID, AUTHOR_GUID, STATUS, CREATED_TIME, CLIENT_DATA_GUID]

    @staticmethod
    def get_reservation_list(author_guid: str):
        params = (author_guid, )
