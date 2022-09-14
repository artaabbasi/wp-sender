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
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from . import models, permissions, serializers
import pika 
import json


@csrf_exempt
@permission_classes((perms.AllowAny))
@api_view(['POST'])
def sendmessage(request):
   token = request.data.get('token', "")
   try:
      token_obj = models.Tokens.objects.get(token=token)
      if token_obj.is_active:
         pass
      else:
            return Response(status=403)
   except :
      return Response(status=403)

   datas = request.data['data']
   messages = []
   for data in datas:
      messages.append(data)
   connection = pika.BlockingConnection(
   pika.ConnectionParameters(host='localhost'))
   channel = connection.channel()
   channel.queue_declare(queue='hello')
   for message in messages:
      media = None
      models.SendMessage.objects.create(user_id=message.get('user', 0), text=message['text'], notif_history_id=message.get('notif_history', 0))
      try:
         media_obj = models.MessageFile.objects.get(pk=int(message['media']))
         media = media_obj.image.path
      except:
         media = None
      for phone in  message.get('phones', []):
         value = {
            "phone" : f"{phone}",
            "text" : f"{message['text']}",
            "user" : message.get('user', 0),
            "notif_history" : message.get('notif_history', 0),
         }
         value.update({"media" : f"{media}"}) if media is not None else None
         value  = json.dumps(value)

         channel.basic_publish(exchange='', routing_key='hello', body=value)
   connection.close()

   return Response({"message": "messages sended"})


class FileUpload(generics.ListCreateAPIView):
   serializer_class = serializers.FileSerializer

   def get_queryset(self):
        return models.MessageFile.objects.all()



@csrf_exempt
@permission_classes((perms.AllowAny))
@api_view(['POST'])
def accept_message(request):
   user = request.data.get('user')
   text = request.data.get('text')
   notif_history = request.data.get('notif_history')
   queryset = models.SendMessage.objects.filter(user_id = user, text=text, notif_history_id=notif_history, sended=False)
   obj = queryset.first()
   obj.sended = True
   obj.save()
   return Response(status=200)


@permission_classes((perms.AllowAny,))
class SendMessageList(generics.ListAPIView):
   serializer_class = serializers.SendMessageSerializer

   def get_queryset(self):
      notif_history = self.kwargs['notif_history']
      return models.SendMessage.objects.filter(notif_history_id=notif_history)

   @csrf_exempt
   def get(self, request, *args, **kwargs):
      return self.list(request, *args, **kwargs)