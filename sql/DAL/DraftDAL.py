from model.json_result import json_format
from model.result import Result
from sql.DAL.userDAL import User
from sql.DB import call_sp
from sql.const_value.const_sp import SP


class Draft:
    MHUB_EMAIL       = 'MhubEmail'      
    MHUB_PASSWORD    = 'MhubPassword'    
    PROJECT_NAME     = 'ProjectName'     
    BLOCK_NAME       = 'BlockName'       
    UNIT_NAME        = 'UnitName'        
    IDENTITY_TYPE    = 'IdentityType'
    IDENTITY_NUMBER  = 'IdentityNumber'
    TITLE            = 'Title'
    FULL_NAME        = 'FullName'
    PREFERRED_NAME   = 'PreferredName'
    CLIENTEMAIL      = 'ClientEmail'
    COUNTRY_CODE     = 'CountryCode'
    MOBILE           = 'Mobile'
    ADDRESS          = 'Address'
    POSTCODE         = 'PostCode'
    CITY             = 'City'
    STATE            = 'State'
    COUNTRY          = 'Country'
    FIRST_TIME       = 'FirstTime'
    PAYMENT_DATE     = 'PaymentDate'
    AGENCY_CMP       = 'AgencyCmp'
    AGENT_NAME       = 'AgentName'
    AGENT_PHONE      = 'AgentPhone'
    REMARKS          = 'Remarks'
    CREATED_TIME     = 'CreatedTime'
    AUTHOR_GUID      = 'AuthorGUID'
    GUID             = 'GUID'
    DRAFTSTATUS      = 'DraftStatus' 

    LIST_COLUMNS = [FULL_NAME, CLIENTEMAIL, CREATED_TIME, GUID, DRAFTSTATUS]

    DETAILS_COLUMNS = [
        MHUB_EMAIL,       
        MHUB_PASSWORD,    
        PROJECT_NAME,     
        BLOCK_NAME,       
        UNIT_NAME,             
        IDENTITY_TYPE,
        IDENTITY_NUMBER,
        TITLE,
        FULL_NAME,
        PREFERRED_NAME,
        CLIENTEMAIL,
        COUNTRY_CODE,
        MOBILE,
        ADDRESS,
        POSTCODE,
        CITY,
        STATE,
        COUNTRY,
        FIRST_TIME,
        PAYMENT_DATE,
        AGENCY_CMP,
        AGENT_NAME,
        AGENT_PHONE,
        REMARKS,
        CREATED_TIME,  
        GUID,  
        AUTHOR_GUID 
    ]

    @staticmethod
    def get_draft_list(author_guid: str):
        params = (author_guid,)
        result = call_sp(SP.SP_Draft_Get_List, params, Draft.LIST_COLUMNS)
        data = []

        if result.is_success():
            data = result.table[Draft.LIST_COLUMNS].to_dict('records')

        return json_format(result, data)

    @staticmethod
    def get_draft_details(draft_guid: str):
        params = (draft_guid,)
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
