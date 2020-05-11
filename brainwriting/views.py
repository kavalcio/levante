from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.template import loader
from .models import Question, Response, Comment
import json

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
    nomination = request.POST['nomination']
    responseToUp = request.POST['response']
    if(nomination == "yes"):
        temp = Response.objects.get(response_text=responseToUp)
        temp.nominations = 1 
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

#only sends back an idea that has not been nominated yet
def get_response(request):
    responses = Response.objects.filter()
    # if(Response.objects.all().count()==0):
    #     return HttpResponse("#-----objects not found-------#")
    # #sends code if all ideas have been nominated
    # if(not response):
    #     return HttpResponse("NULL869")
    return HttpResponse(responses.order_by('?').first())

def get_response_and_comments(request):
    if not request.is_ajax() or not request.method=='GET':
        return HttpResponseNotAllowed(['GET'])

    responses = Response.objects.filter()

    response = responses.order_by('?').first()
    comments = Comment.objects.filter(response=response)

    obj = {
        "response": response.response_text,
        "comments": []
    }

    for comment in comments:
        obj['comments'].append(comment.comment_text)

    return HttpResponse(json.dumps(obj))

def add_comment(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    idea = request.POST['idea']
    comment = request.POST['comment']

    responseObj = Response.objects.get(response_text=idea)

    commentObj = Comment(
        response=responseObj,
        comment_text=comment
    )

    commentObj.save()

    return HttpResponse()
