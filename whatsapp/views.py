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


loggin = False

def _loggin():
   global loggin
   if not loggin:
      global driver
      driver = webdriver.Chrome("/home/arta/Downloads/chromedriver_linux64/chromedriver")
      driver.get("https://web.whatsapp.com")
      print("Scan QR Code, And then Enter")
      input()
      print("Logged In")
      loggin = True

@permission_classes((permissions.SendMessageAccess))
@api_view(['POST'])
def sendmessage(request , id):
   global driver
   _loggin()
   message_obj = models.SendMessage.objects.get(id=id)
   contacts, text = message_obj.phones.all(), message_obj.text
   for contact in contacts:
      driver.get(f"https://web.whatsapp.com/send?phone={contact}&text={text}")
      inp_xpath = '//div[@title="Type a message"]'
      input_box = WebDriverWait(driver,50).until(lambda driver: driver.find_element(by=By.XPATH, value=inp_xpath))
      time.sleep(2)
      input_box.send_keys(Keys.ENTER)
      time.sleep(2)
         

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