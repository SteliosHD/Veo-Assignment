from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(["GET"])
def index(request):
    # dummy index view
    response = {
        "message": "Server is up and running",
        "status": 200,
    }
    return Response(response)
