from rest_framework import serializers
from . import models

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MessageFile
        fields = "__all__"

