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
        return Draft.get_draft_details(draft_guid)


@csrf_exempt
def post_draft_data(request):
    if request.method == "POST":
        params = get_params(request.POST)
        return Draft.create_draft_details(params)


@csrf_exempt
def update_draft_details(request):
    if request.method == "POST":
        req = request.POST
        draft_guid = req.get('DraftGuid')
        params = (draft_guid,) + get_params(req)        
        return Draft.update_draft_details(params)


def get_params(req):

    params = (
        req.get('AuthorGuid'),
        req.get('IdentityType'),
        req.get('IdentityNumber'),
        req.get('Title'),
        req.get('FullName'),
        req.get('PreferredName'),
        req.get('Email'),
        req.get('Mobile'),
        req.get('Address'),
        req.get('Postcode'),        
        req.get('City'),
        req.get('State'),
        req.get('FirstTime'),
        req.get('PaymentDate'),
        req.get('AgencyCmp'),
        req.get('AgentName'),
        req.get('AgentPhone'),
        req.get('Remarks')
    )

    return params


@csrf_exempt
def delete_draft_data(request):
    if request.method == "POST":
        req = request.POST
        draft_guid = req.get('draft_guid')  
        return Draft.delete_draft_data((draft_guid,))