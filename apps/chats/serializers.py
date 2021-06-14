from rest_framework import serializers

class SendChatMessageSerializer(serializers.Serializer):
    name = serializers.CharField()
    message = serializers.CharField()
    timestamp = serializers.DateTimeField()
    profile_pic = serializers.ImageField() 