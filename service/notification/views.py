from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from .tasks import check_send


def newsletter(request):
    check_send()
    return HttpResponse("test")