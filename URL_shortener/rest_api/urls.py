from django.urls import path
from rest_framework import routers

from .views import *

urlpatterns = [
    path('<str:short_url>/', redirect_link, name='redirectlink'),
    path('api/v0/addlink/', add_real_url, name='addlink'),
    path('api/v0/<str:name>/', get_real_url, name='getrealurl')
]
