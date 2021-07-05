from apps.images.specs import Image256x256, Image36x36
from apps.images.serializers import ImageSpecField
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    profile_pic = ImageSpecField(specs={
        'image_256x256' : Image256x256,
        'image_36x36' : Image36x36,
    }, base=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'profile_pic')
        read_only_fields = ('email',)

