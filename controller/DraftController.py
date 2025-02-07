from django.views.decorators.csrf import csrf_exempt

from sql.DAL.DraftDAL import Draft


@csrf_exempt
def get_client_data_list(request):
    if request.method == "GET":
        guid = request.GET.get('guid')
        return Draft.get_client_data_list(guid)


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

        return Draft.insert_client_data(params)
