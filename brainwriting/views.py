from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.template import loader
from .models import Room, Question, Response, Comment
from django.utils.crypto import get_random_string
import string

# Create your views here.

def index(request):
    return render(request, 'brainwriting/index.html')

def room(request, room_name, user_name):
    return render(request, 'brainwriting/room.html', {
        'room_name': room_name,
        'user_name': user_name
    })

def inspiration(request, room_name, user_name):
    return render(request, 'brainwriting/inspiration.html', {
        'room_name': room_name,
        'user_name': user_name
    })

def nominate(request, room_name, user_name):
    return render(request, 'brainwriting/nominate.html', {
        'room_name': room_name,
        'user_name': user_name
    })

def development(request, room_name, user_name):
    return render(request, 'brainwriting/development.html', {
        'room_name': room_name,
        'user_name': user_name
    })

def voting(request, room_name, user_name):
    return render(request, 'brainwriting/voting.html', {
        'room_name': room_name,
        'user_name': user_name
    })


# HTTP endpoints #

def add_question(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    questionObject = Question(
        question_text=request.POST['problem'],
        pub_date='2000-11-11'
    )

    questionObject.save()

    return HttpResponse(request.session)

def upd_response(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    
    #Ensuring the expected variables are in the POST request
    if "nomination" in request.POST:  
        nomination = request.POST['nomination']
    else:
        nomination = "none"
    if "response" in request.POST:
        responseToUp = request.POST['response']
    else: 
        responseToUp = "none"
    if "developed" in request.POST:
        developed = request.POST['developed']
    else:
        developed = "none"
    if "voted" in request.POST:
        voted = request.POST['voted']
    else:
        voted = "none"    

    if(developed == "yes"):
        temp = Response.objects.get(response_text=responseToUp)
        temp.developed = 2 
        temp.save()
    if(voted == "yes"):
        temp = Response.objects.get(response_text=responseToUp)
        temp.voted = 1 
        temp.save()
    elif(voted == "no"):
        temp = Response.objects.get(response_text=responseToUp)
        temp.voted = 2
        temp.save()       
    if(nomination == "yes"):
        temp = Response.objects.get(response_text=responseToUp)
        temp.nominations = 1 
        temp.save()
    elif(nomination == "no"):
        temp = Response.objects.get(response_text=responseToUp)
        temp.nominations = 2 
        temp.save()
    
    return HttpResponse(request.session)

def add_response(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    questionName = request.POST['problem']
    questionObj = Question.objects.get(question_text=questionName)

    responseObj = Response(
        question=questionObj,
        response_text=request.POST['message'],
        nominations=0
    )

    responseObj.save()

    return HttpResponse(request.session)

def get_response(request, page):
    #if request is from the nominate page only returns an idea that has not been nominated yet
    if(page == "nominate"):
         response = Response.objects.filter(nominations = 0)
         #sends error code if all ideas have been nominated
         if(not response):
           return HttpResponse("NULL869")
    elif(page == "development"):
        response = Response.objects.filter(developed = 0)
        if(not response):
           return HttpResponse("NULL869")
    elif(page == "voting"):
        response = Response.objects.filter(voted = 0)
        if(not response):
           return HttpResponse("NULL869")       
    else:
        response = Response.objects.filter()

    return HttpResponse(response.order_by('?').first())

def add_comment(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    idea = request.POST['idea']
    comment = request.POST['comment']

    responseObj = Response.objects.get(response_text=idea)
    responseObj.developed = 1 
    responseObj.save()

    commentObj = Comment(
        response=responseObj,
        comment_text=comment
    )

    commentObj.save()

    return HttpResponse()

def create_room(request):
    roomKey = get_random_string(length = 5, allowed_chars = (string.ascii_uppercase + string.digits))
    keyExists = Room.objects.filter(room_key=roomKey, active=True).exists()

    while (keyExists):
        roomKey = get_random_string(length = 5, allowed_chars = (string.ascii_uppercase + string.digits))
        keyExists = Room.objects.filter(room_key=roomKey, active=True).exists()

    roomObj = Room(
        room_key=roomKey,
        active=True,
    )

    roomObj.save()

    return HttpResponse(roomKey)

def join_room(request):
    roomKey = request.POST['roomKey']
    roomExists = Room.objects.filter(room_key=roomKey, active=True).exists()

    if (roomExists):
        roomExists = 1
    else:
        roomExists = 0

    return HttpResponse(roomExists)