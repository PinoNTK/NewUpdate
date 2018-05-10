from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def candidate(request):
    """ A view that display an article based on his ID"""
    text = "Displaying article Number "
    return HttpResponse(text)
