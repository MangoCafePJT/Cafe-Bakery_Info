import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    # Receive message from WebSocket


    def receive(self, text_data):
        username = self.scope["user"].username
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"{username} : {message} ({timestamp})"
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = self.scope["user"].username

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            # 'timestamp': timezone.now().isoformat()
        }))

# import json

# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         self.send(text_data=json.dumps({"message": message}))