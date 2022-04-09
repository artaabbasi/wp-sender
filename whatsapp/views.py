import datetime
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

from rest_framework import generics
from rest_framework import permissions as perms
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from . import models, permissions, serializers
import pika 
import json

loggin = False

connection = pika.BlockingConnection(
   pika.ConnectionParameters(host='localhost'))
global channel
channel = connection.channel()
channel.queue_declare(queue='hello')



@permission_classes((perms.IsAuthenticated))
@api_view(['POST'])
def sendmessage(request):
   datas = request.data['data']
   messages = []
   for data in datas:
      messages.append(data)
   connection = pika.BlockingConnection(
   pika.ConnectionParameters(host='localhost'))
   channel = connection.channel()
   channel.queue_declare(queue='hello')
   for message in messages:
      for phone in  message.get('phones'):
         value = {
            "phone" : f"{phone}",
            "text" : f"{message['text']}",
            "media" : f"{message['media']}",
         }

         value  = json.dumps(value)

         channel.basic_publish(exchange='', routing_key='hello', body=value)
   connection.close()

   return Response({"message": "messages sended"})



class Retrievemessage(generics.RetrieveUpdateDestroyAPIView):
   serializer_class = serializers.SendMessageSerializer
   lookup_field = 'id'

   def get_queryset(self):
        return models.SendMessage.objects.all()
        
class Createmessage(generics.ListAPIView):
   serializer_class = serializers.SendMessageSerializer
   permission_classes = [perms.IsAuthenticated,]
   def get_queryset(self):
      return models.SendMessage.objects.all()

class Createphone(generics.ListCreateAPIView):
    serializer_class = serializers.PhoneSerializer

    def get_queryset(self):
        return models.Phone.objects.all()