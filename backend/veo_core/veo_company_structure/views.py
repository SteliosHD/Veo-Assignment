from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    # dummy index view
    html = "<html><body><h1>Index Page</h1></body></html>"
    return HttpResponse(html)
