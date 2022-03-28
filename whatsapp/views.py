import datetime
import time

import pywhatkit
import pyautogui as pg

import webbrowser as web
from pyvirtualdisplay import Display
from rest_framework import generics
from rest_framework import permissions as perms
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from . import models, permissions, serializers


@permission_classes((permissions.SendMessageAccess))
@api_view(['POST'])
def sendmessage(request , id):
   print("sending")
   if request.method == 'POST':
      serializer = serializers.SendMessageSerializer
      obj = models.SendMessage.objects.get(id = id)
      phone_list = []
      y= obj.phones.all()

      for i in y:
         phone_list.append(i.phone)
      print(phone_list)
      
      for t in phone_list:  
         x = datetime.datetime.now()
         pywhatkit.sendwhatmsg_instantly(t,obj.text, wait_time=10)
         pg.press("enter")
         time.sleep(15)
         


   return Response({"message": "messages sended"})

class Retrievemessage(generics.RetrieveUpdateDestroyAPIView):
   serializer_class = serializers.SendMessageSerializer
   lookup_field = 'id'

   def get_queryset(self):
        return models.SendMessage.objects.all()
        
class Createmessage(generics.ListCreateAPIView):
    serializer_class = serializers.SendMessageSerializer

    def get_queryset(self):
        return models.SendMessage.objects.all()

class Createphone(generics.ListCreateAPIView):
    serializer_class = serializers.PhoneSerializer

    def get_queryset(self):
        return models.Phone.objects.all()