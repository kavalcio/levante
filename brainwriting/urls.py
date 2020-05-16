from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_response/', views.add_response, name='add_response'),
    path('get_response_and_comments/', views.get_response_and_comments, name='get_response_and_comments'),
    path('get_response/<str:page>', views.get_response, name='get_response'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_question/', views.add_question, name='add_question'),
    path('get_question/', views.get_question, name='get_question'),
    path('upd_response/', views.upd_response, name='upd_response'),
    path('create_room/', views.create_room, name='create_room'),
    path('join_room/', views.join_room, name='join_room'),

    path('<str:room_name>/admin/', views.roomCreate, name='roomCreate'),
    path('<str:room_name>/admin/code', views.roomCode, name='roomCode'),
    path('<str:room_name>/<str:user_name>/', views.room, name='room'),
    path('<str:room_name>/<str:user_name>/inspiration/', views.inspiration, name='inspiration'),
    path('<str:room_name>/<str:user_name>/nominate/', views.nominate, name='nominate'),
    path('<str:room_name>/<str:user_name>/development/', views.development, name='development'),
    path('<str:room_name>/<str:user_name>/voting/', views.voting, name='voting'),
]