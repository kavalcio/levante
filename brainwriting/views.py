from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.template import loader
from .models import Question

# Create your views here.

def index(request):
    return render(request, 'brainwriting/index.html')

def room(request, room_name, user_name):
    return render(request, 'brainwriting/room.html', {
        'room_name': room_name,
        'user_name': user_name
    })
