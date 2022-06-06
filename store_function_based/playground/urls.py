from django.urls import path, include
from . import views


# URLConf
urlpatterns = [
    path('hello/', views.say_hello)
]


