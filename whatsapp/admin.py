from django.contrib import admin
from . import models

admin.site.register(models.SendMessage)
admin.site.register(models.Phone)
admin.site.register(models.Tokens)