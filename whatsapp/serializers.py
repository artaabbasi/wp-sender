from rest_framework import serializers
from . import models

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phone
        fields = "__all__"

class SendMessageSerializer(serializers.ModelSerializer):
    phones_obj = PhoneSerializer(source='phones', many=True, read_only=True)
    class Meta:
        model = models.SendMessage
        fields = '__all__'

