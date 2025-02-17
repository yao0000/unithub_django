from model.json_result import json_format
from model.result import Result
from sql.DAL.userDAL import User
from sql.DB import call_sp
from sql.const_value.const_sp import SP


class Draft:
    TITLE = 'Title'
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
    GUID = 'GUID'

    LIST_COLUMNS = [NAME, EMAIL, GUID]

    DETAILS_COLUMNS = [TITLE, NAME, EMAIL, MOBILE,
                       ADDRESS, POSTCODE, CITY, STATE, PAYMENT_DATE, AGENCY_CMP,
                       AGENT_NAME, AGENT_PHONE, REMARKS, FIRST_TIME,
                       CREATED_TIME, GUID, User.PASSWORD]

    @staticmethod
    def get_draft_list(author_guid: str):
        params = (author_guid,)
        result = call_sp(SP.SP_Draft_Get_List, params, Draft.LIST_COLUMNS)
        data = []

        if result.is_success():
            data = result.table[[Draft.NAME, Draft.EMAIL, Draft.GUID]].to_dict('records')

        return json_format(result, data)

    @staticmethod
    def get_draft_details(draft_guid: str, author_guid: str):
        params = (draft_guid, author_guid)
        result = call_sp(SP.SP_Draft_Get_Details, params, Draft.DETAILS_COLUMNS)
        data = []
        if result.is_success():
            data = result.table[Draft.DETAILS_COLUMNS].to_dict('records')

        return json_format(result, data)

    @staticmethod
    def create_draft_details(params):
        result = call_sp(SP.SP_Draft_Create, params)
        return json_format(result)

    @staticmethod
    def update_draft_details(params):
        result = call_sp(SP.SP_Draft_Update, params)
        return json_format(result)

    @staticmethod
    def delete_draft_data(params):
        result = call_sp(SP.SP_Draft_Delete, params)
        return json_format(result)
