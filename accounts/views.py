from rest_framework import generics
from rest_framework import permissions as perms
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from . import models
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def login(request):
    tlid = request.data.get('telegram_id')
    user = get_user_model().objects.get(telegram_id=tlid)
    refresh = RefreshToken.for_user(user)
    data = {}
    data['refresh'] = str(refresh)
    data['access'] = str(refresh.access_token)
    return Response(data)
    
