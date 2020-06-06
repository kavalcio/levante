from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.template import loader
from django.utils.crypto import get_random_string
from .models import Room, Question, Response, Comment
from django.core import serializers
import string
import json

# Create your views here.

def index(request):
    return render(request, 'brainwriting/index.html')

def roomCreate(request, room_name):
    return render(request, 'brainwriting/roomCreate.html', {
        'room_name': room_name
    })

def roomCode(request, room_name):
    return render(request, 'brainwriting/roomCode.html', {
        'room_name': room_name
    })

def room(request, room_name, user_name, room_num):
    return render(request, 'brainwriting/room.html', {
        'room_name': room_name,
        'user_name': user_name,
        'room_num': room_num
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

def get_question(request):
    roomObj = Room.objects.get(room_id = request.GET['room_id'])
    questionObj = Question.objects.get(room = roomObj)

    return HttpResponse(questionObj)

def add_question(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    roomObj = Room.objects.get(room_id = request.POST['room_id'])

    questionObject = Question(
        room = roomObj,
        question_text = request.POST['problem'],
        pub_date = '2000-11-11'
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

    roomObj = Room.objects.get(room_id = request.POST['room_id'])

    responseObj = Response(
        room=roomObj,
        response_text=request.POST['message'],
        nominations=0
    )

    responseObj.save()

    return HttpResponse(request.session)

def get_comments(request):
    if not request.is_ajax() or not request.method=='GET':
        return HttpResponseNotAllowed(['GET'])

    responseId = request.GET['response_id']

    response = Response.objects.filter(id=responseId).first()

    comments = Comment.objects.filter(response=response)

    obj = {
        "comments": []
    }

    for comment in comments:
        obj['comments'].append(comment.comment_text)

    return HttpResponse(json.dumps(obj))

def get_responses(request):
    if not request.is_ajax() or not request.method=='GET':
        return HttpResponseNotAllowed(['GET'])

    # Get input parameters
    page = request.GET['page']
    roomId = request.GET['room_id']

    room = Room.objects.get(room_id = roomId)

    if (page == "nominate"):
        responses = Response.objects.filter(room = room, nominations = 0)
    elif (page == "development"):
        responses = Response.objects.filter(room = room, developed = 0)
    elif (page == "voting"):
        responses = Response.objects.filter(room = room, voted = 0)
    else:
        responses = Response.objects.filter(room = room)

    #sends error code if all ideas have been nominated
    if (not responses):
        return HttpResponse("NULL869")

    serializedResponse = serializers.serialize('json', responses)

    return HttpResponse(serializedResponse)

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
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    roomKey = get_random_string(length = 5, allowed_chars = (string.ascii_uppercase + string.digits))
    keyExists = Room.objects.filter(room_key=roomKey, active=True).exists()

    while (keyExists):
        roomKey = get_random_string(length = 5, allowed_chars = (string.ascii_uppercase + string.digits))
        keyExists = Room.objects.filter(room_key=roomKey, active=True).exists()

    isTutorial = request.POST['is_tutorial']

    roomObj = Room(
        room_key = roomKey,
        active = True,
        is_tutorial = isTutorial
    )

    roomObj.save()

    serialized_object = serializers.serialize('json', [roomObj])

    return HttpResponse(serialized_object)

def join_room(request):
    roomKey = request.POST['roomKey']
    roomExists = Room.objects.filter(room_key=roomKey, active=True).exists()

    if (roomExists):
        roomExists = 1
    else:
        roomExists = 0

    return HttpResponse(roomExists)