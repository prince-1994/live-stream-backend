from apps.chats.models import Message
import json
from os import close, sync
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from apps.shows.models import Show
from apps.chats.serializers import SendChatMessageSerializer


class ShowConsumer(JsonWebsocketConsumer):
    def chat_send_message(self, data):
        message = data.get('message')
        if self.user.is_anonymous or not message:
            print(data)
        else:
            message = Message.objects.create(user=self.user, show=self.show, content=message)
            first_name = self.user.first_name or "" 
            last_name = self.user.last_name or ""
            name =  f"{first_name} {last_name}"
            data = {
                'name' : name,
                'message' : message.content,
                'timestamp': str(message.timestamp),
                'profile_pic' : self.user.profile_pic.url,
            }
            print(data)
            self.send_json(data)
    
    def chat_load_messages(self, data):
        no_of_messages = data.get("no_of_messages") 
        last_timestamp = data.get("last_timestamp")
        if not no_of_messages or not last_timestamp:
            self.send_json({"error" : "either no_of_messages or last_timestamp is missing"})
        elif no_of_messages > 20:
            self.send_json({"error" : "no_of_messages can not be greater than 20"})
        messages = self.show.messages.filter(timestamp__lt=last_timestamp).order_by('-timestamp').all()[:no_of_messages]
        message_data = []
        
        for message in messages:
            author = message.user
            name = (author.first_name or "") + (author.last_name or "")
            message_data.append({
                'name' : name,
                'message' : message.content,
                'timestamp': str(message.timestamp),
                'profile_pic' : author.profile_pic.url,
            })
        # print(messages)
        self.send_json(message_data)

    commands = {
        'chat_send_message' : chat_send_message,
        'chat_load_messages' : chat_load_messages
    }

    def connect(self):
        show_id = self.scope["url_route"]["kwargs"]["show_id"]
        self.user = self.scope['user']
        try:
            self.show = Show.objects.get(pk=show_id)
            
            self.show_ws_group_name = f"ws_{self.show.name}_{self.show.id}"
            async_to_sync(self.channel_layer.group_add)(
                self.show_ws_group_name, self.channel_name
            )
            self.accept()
        except Exception as e:
            print(e)
            self.close()


    def disconnect(self, close_code):
        print(self.scope)
        async_to_sync(self.channel_layer.group_discard)(
            self.show_ws_group_name, self.channel_name
        )

    def receive_json(self, data):
        command_type = data.get('command')
        if not command_type:
            self.send_json({'error' : 'Command type not found'})
        handler = self.commands.get(command_type)
        if handler:
            handler(self, data)
        else:
            self.send_json({"error" : "Handler not found for command type"})