from model.json_result import json_format
from model.result import Result
from sql.DB import call_sp
from sql.const_value.const_sp import SP


class Client:
    ID = 'ID'
    IDENTITY = 'Identity'
    NAME = 'Name'
    EMAIL = 'Email'
    MOBILE = 'Mobile'
    FIRST_TIME = 'FirstTime'
    ADDRESS = 'Address'
    POSTCODE = 'PostCode'
    CITY = 'City'
    STATE = 'State'
    PAYMENT_DATE = 'PaymentDate'
    AGENCY_CMP = 'AgencyCmp'
    AGENT_NAME = 'AgentName'
    AGENT_PHONE = 'AgentPhone'
    REMARKS = 'Remarks'
    CREATED_TIME = 'CreatedTime'
    AUTHOR_GUID = 'AuthorGUID'

    TABLE_COLUMNS = [Result.MESSAGE, Result.RESPONSE, ID, IDENTITY, NAME, EMAIL, MOBILE, FIRST_TIME,
                     ADDRESS, POSTCODE, CITY, STATE, PAYMENT_DATE, AGENCY_CMP,
                     AGENT_NAME, AGENT_PHONE, REMARKS, CREATED_TIME, AUTHOR_GUID]

    @staticmethod
    def get_client_data_list(guid: str):
        params = (guid, )
        result = call_sp(SP.SP_Client_Get_Client_Data_Summary, params, Client.TABLE_COLUMNS)
        data = []

        if result.is_success():
            data = result.table[Client.ID].tolist()

        return json_format(result, data)

    @staticmethod
    def insert_client_data(params):
        result = call_sp(SP.SP_Client_Create_Client_Data, params, Result.COLUMNS)
        return json_format(result)
