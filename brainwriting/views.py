from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.template import loader
from .models import Question, Response

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

def add_question(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    questionObject = Question(
        question_text=request.POST['problem'],
        pub_date='2000-11-11'
    )

    questionObject.save()

    return HttpResponse(request.session)

def add_response(request):
    print(request)
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
