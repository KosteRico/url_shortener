from django.urls import path
from rest_framework import routers

from .views import add_real_url, get_real_url

urlpatterns = [
    path('addlink/', add_real_url, name='addlink'),
    path('<str:name>/', get_real_url, name='getrealurl')
]
