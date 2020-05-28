from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.template import loader
from django.utils.crypto import get_random_string
from .models import Room, Question, Response, Comment
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
def end(request, room_name, user_name):
    return render(request, 'brainwriting/end.html', {
        'room_name': room_name,
        'user_name': user_name
    })


# HTTP endpoints #

def get_question(request):
    response = Question.objects.filter()

    return HttpResponse(response.order_by('?').first())

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
    if "check" in request.POST:  
        check = request.POST['check']
    else:
        check = "none"
    responseToUp = request.POST['response']

    if(check == "yes" or check == "nominate" or check == "vote"):
        temp = Response.objects.get(response_text=responseToUp)
        if(check == "nominate"):
            temp.voteNum = 1
        if(check == "vote"):
            temp.voteNum = temp.voteNum + 1
        temp.check = 1 
        temp.save()
    elif(check == "no"):
        temp = Response.objects.get(response_text=responseToUp)
        temp.check = 2
        temp.save()       
    
    return HttpResponse(request.session)

def reset_responses(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    for temp in Response.objects.all():
        temp.check = 0
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
    )

    responseObj.save()

    return HttpResponse(request.session)

def get_response_and_comments(request):
    if not request.is_ajax() or not request.method=='GET':
        return HttpResponseNotAllowed(['GET'])

    responses = Response.objects.filter(check = 0)
    if(not responses):
           return HttpResponse("NULL869")

    response = responses.order_by('?').first()
    comments = Comment.objects.filter(response=response)

    obj = {
        "response": response,
        "comments": []
    }

    for comment in comments:
        obj['comments'].append(comment.comment_text)

    return HttpResponse(json.dumps(obj))

def get_response(request, page):
    #if request is from the nominate page only returns an idea that has not been nominated yet
    if(page == "nominate" or page == "development"):
         response = Response.objects.filter(check = 0)
         #sends error code if all ideas have been nominated
         if(not response):
           return HttpResponse("NULL869")
    elif(page == "voting"):
        response = Response.objects.filter(voteNum = 1)
        temp = response.order_by('?').first()
        #sends error code if all ideas have been nominated
        if(not response or temp.check != 0):
           return HttpResponse("NULL869")
    elif(page == "end"):
        response = Response.objects.exclude(voteNum = 0)
        print(response)
        temp2 = response.order_by('-voteNum')
        temp = response.order_by('-voteNum').first()
        print(temp2)
        print(temp.check)
        #sends error code if all ideas have been nominated
        if(not response or temp.check != 0):
           return HttpResponse("NULL869")
        return HttpResponse(temp2)
    else:
        response = Response.objects.filter()

    return HttpResponse(response.order_by('?').first())

def add_comment(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    idea = request.POST['idea']
    comment = request.POST['comment']

    responseObj = Response.objects.get(response_text=idea)
    responseObj.check = 1 
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