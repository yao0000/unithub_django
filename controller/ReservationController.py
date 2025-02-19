from django.views.decorators.csrf import csrf_exempt

from sql.DAL.ReservationDAL import Reservation


@csrf_exempt
def get_reservation_list(request):
    if request.method == "GET":
        req = request.GET
        author_guid = req.get("author_guid")
        return Reservation.get_reservation_list(author_guid)


@csrf_exempt
def post_reservation(request):
    if request.method == "POST":
        req = request.POST
        author_guid = req.get("author_guid")
        status = req.get("status")
        draft_guid = req.get("draft_guid")

        return Reservation.create_reservation(author_guid, status, draft_guid)
