from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.template import loader
from django.core import serializers
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
def end(request, room_name, user_name):
    return render(request, 'brainwriting/end.html', {
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
    if "check" in request.POST:  
        check = request.POST['check']
    else:
        check = "none"
    responseToUp = request.POST['response']

    temp = Response.objects.get(response_text=responseToUp)
    if(check == "nominate"):
        temp.voteNum = 1
    if(check == "vote"):
        temp.voteNum = temp.voteNum + 1   
    
    temp.save()
    return HttpResponse(request.session)

def add_response(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    roomObj = Room.objects.get(room_id = request.POST['room_id'])

    responseObj = Response(
        room=roomObj,
        response_text=request.POST['message'],
        user_id=request.POST['user_id'],
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

    if (page == "development" or page == "voting"):
        responses = Response.objects.filter(room = room, voteNum = 1)
    elif(page == "end"):
        temp = Response.objects.filter(room = room).exclude(voteNum = 0)
        responses = temp.order_by('-voteNum')
    else:
        responses = Response.objects.filter(room = room)

    #sends error code if no ideas were found
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

    # If the user wants to start a tutorial, join the existing tutorial room or create a new one
    if roomKey == 'TUTORIAL':
        # Create the tutorial room
        roomObj = Room(
            room_key = roomKey,
            active = True,
            is_tutorial = True
        )
        roomObj.save()

        # Create the tutorial question
        questionObject = Question(
            room = roomObj,
            question_text = 'How might we make video conferencing meetings shorter and more effective through software changes?',
            pub_date = '2000-11-11'
        )
        questionObject.save()

        # Create full list of tutorial responses
        responseList = [
            'Make the software force people to take turns speaking',
            'Incorporate gamification to encourage valuable comments',
            'Have a "meeting notes" feature that the assigned person fills out',
            'Provide Ice breaker questions or games to participants',
            'Add a "take a break" feature that pauses the meeting and resumes in 3 minutes',
            'Display meeting goals on the side of the screen at all times',
            'Add timers to how long people have to speak and make people "raise their hand" to be unmuted'
        ]
        for responseText in responseList:
            responseObj = Response(
                room=roomObj,
                response_text=responseText,
                user_id='-1',
            )
            responseObj.save()

        returnVal = serializers.serialize('json', [roomObj])
            
        return HttpResponse(returnVal)
    else:
        roomObj = Room.objects.filter(room_key=roomKey, active=True)

        if (roomObj):
            returnVal = serializers.serialize('json', roomObj)
        else:
            returnVal = None

    return HttpResponse(returnVal)

def add_user_to_room(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    roomId = request.POST['room_id']
    room = Room.objects.get(room_id = roomId)
    roomUserList = json.loads(room.user_list)

    userId = get_random_string(length = 2, allowed_chars = (string.digits))

    while (userId in roomUserList):
        userId = get_random_string(length = 2, allowed_chars = (string.digits))

    roomUserList[len(roomUserList)] = userId
    roomUserList = json.dumps(roomUserList)
    room.user_list = roomUserList
    room.save()

    return HttpResponse(userId)