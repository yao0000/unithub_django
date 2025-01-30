from django.views.decorators.csrf import csrf_exempt

from sql.DAL.ClientDataDAL import Client


@csrf_exempt
def get_client_data_list(request):
    if request.method == "GET":
        guid = request.GET.get('guid')
        return Client.get_client_data_list(guid)


@csrf_exempt
def post_client_data(request):
    if request.method == "POST":
        req = request.POST

        params = (
            req.get('Identity'),
            req.get('Name'),
            req.get('Email'),
            req.get('Mobile'),
            req.get('FirstTime'),
            req.get('Address'),
            req.get('Postcode'),
            req.get('City'),
            req.get('State'),
            req.get('PaymentDate'),
            req.get('AgencyCmp'),
            req.get('AgentName'),
            req.get('AgentPhone'),
            req.get('Remarks'),
            req.get('AuthorGuid')
        )

        return Client.insert_client_data(params)
