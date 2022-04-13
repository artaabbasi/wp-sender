from django.db import models
from django.contrib.auth import get_user_model

class Phone(models.Model):
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.phone

class SendMessage(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:30]

class MessageFile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()