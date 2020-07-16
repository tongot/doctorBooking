from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('About', views.about),
    path('Contact', views.contact),
]