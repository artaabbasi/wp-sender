from rest_framework import serializers
from . import models

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MessageFile
        fields = "__all__"


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SendMessage
        fields = "__all__"