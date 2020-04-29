from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_response/', views.add_response, name='add_response'),
    path('get_response/', views.get_response, name='get_response'),
    path('add_question/', views.add_question, name='add_question'),
    path('<str:room_name>/<str:user_name>/', views.room, name='room'),
    path('<str:room_name>/<str:user_name>/inspiration/', views.inspiration, name='inspiration'),
]