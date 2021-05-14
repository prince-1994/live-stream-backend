from rest_framework import serializers
from .models import Channel

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'description', 'owner', 'display_pic', 'background_pic')
        read_only_fields = ('owner',)

    # Use this method for the custom field
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def create(self, validated_data):
        user = self._user()
        obj = Channel.objects.create(owner=user,**validated_data)
        obj.save()
        return obj
