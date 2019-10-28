from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import *
from .serializers import LinkSerializer

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


def is_url(url):
    try:
        validate = URLValidator()
        validate(url)
        return True
    except ValidationError:
        return False


@api_view(['POST'])
@permission_classes([ClientOnly])
def add_real_url(request):
    real_url = request.POST['real_url']
    short_url = request.POST['name']

    serializer = LinkSerializer(data=request.data)
    is_ok = True
    for i in request.POST:
        if request.POST[i] == "":
            is_ok *= False

    is_ok &= is_url(real_url)

    is_ok &= (short_url.count('/') == 0)

    if serializer.is_valid() and is_ok:
        serializer.save()
        return Response({'status': 'URL shortcut created!!!'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def redirect_link(request, short_url):
    real_url_model = LinkModel.objects.get(name=short_url)
    if real_url_model is not "" and real_url_model is not None:
        return redirect(real_url_model.real_url)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
