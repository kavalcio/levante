from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.template import loader
# from .models import Question

# Create your views here.

def index(request):
    return HttpResponse("Hello, world.")
