from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_response/', views.add_response, name='add_response'),
    path('get_response/', views.get_response, name='get_response'),
    path('get_response_and_comments/', views.get_response_and_comments, name='get_response_and_comments'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_question/', views.add_question, name='add_question'),
    path('upd_response/', views.upd_response, name='upd_response'),
    path('<str:room_name>/<str:user_name>/', views.room, name='room'),
    path('<str:room_name>/<str:user_name>/inspiration/', views.inspiration, name='inspiration'),
    path('<str:room_name>/<str:user_name>/nominate/', views.nominate, name='nominate'),
    path('<str:room_name>/<str:user_name>/development/', views.development, name='development'),
]