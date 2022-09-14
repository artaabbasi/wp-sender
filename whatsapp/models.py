from django.db import models
from django.contrib.auth import get_user_model

class Phone(models.Model):
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.phone

class SendMessage(models.Model):
    user_id = models.IntegerField()
    notif_history_id = models.IntegerField(default=0)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    sended = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:30]

class MessageFile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()


import uuid
class Tokens(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True )
    is_active = models.BooleanField(default=False)