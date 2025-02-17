from django.views.decorators.csrf import csrf_exempt

from sql.DAL.DraftDAL import Draft


@csrf_exempt
def get_draft_list(request):
    if request.method == "GET":
        author_guid = request.GET.get('author_guid')
        return Draft.get_draft_list(author_guid)


@csrf_exempt
def get_draft_details(request):
    if request.method == "GET":
        draft_guid = request.GET.get('draft_guid')
        author_guid = request.GET.get('author_guid')
        return Draft.get_draft_details(draft_guid, author_guid)


@csrf_exempt
def post_draft_data(request):
    if request.method == "POST":
        params = get_params(request.POST)
        return Draft.create_draft_details(params)


@csrf_exempt
def update_draft_details(request):
    if request.method == "POST":
        req = request.POST
        params = get_params(req) + (req.get('DraftGuid'),)
        return Draft.update_draft_details(params)


def get_params(req):
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

    return params


@csrf_exempt
def delete_draft_data(request):
    if request.method == "POST":
        req = request.POST
        params = (req.get('AuthorGuid'), req.get('DraftGuid'))
        return Draft.delete_draft_data(params)
