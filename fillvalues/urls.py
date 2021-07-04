from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('dayprice/<slug:slug>', views.dayprice),
    path('dataval', views.dataval),
    path('getshareprice', views.getshareprice)

]