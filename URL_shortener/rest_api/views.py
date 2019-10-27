# Create your views here.
import re

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .serializers import LinkSerializer
from .models import *

ALLOWED_ADDRESSES_FOR_REST_API = [
    '127.0.0.1'
]


class ClientOnly(BasePermission):
    def has_permission(self, request, view):
        ip = request.META['REMOTE_ADDR']
        return ip in ALLOWED_ADDRESSES_FOR_REST_API


@api_view(['GET'])
@permission_classes([ClientOnly])
def get_real_url(request, name):
    real_url = LinkModel.objects.get(name=name)
    serializer = LinkSerializer(real_url)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([ClientOnly])
def add_real_url(request):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    real_url = LinkSerializer(data=request.data)
    is_empty = False
    for i in request.POST:
        if request.POST[i] == "":
            is_empty = True
    if real_url.is_valid() and not is_empty and re.match(regex, request.POST['real_url']):
        real_url.save()
        return Response({'status': 'URL shortcut created!!!'}, status=status.HTTP_201_CREATED)
    else:
        return Response(real_url.errors, status=status.HTTP_400_BAD_REQUEST)
