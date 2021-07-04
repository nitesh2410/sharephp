from django.urls import path
from . import views

urlpatterns = [
    path('getavg', views.getAvg),
    path('simple_upload', views.simple_upload)
]