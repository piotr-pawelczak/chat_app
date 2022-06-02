import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from chat.models import ChatMessage
from channels.db import database_sync_to_async
from chat.models import Notification
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']

        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)

        if text_data_json.get('type') == 'notification':
            sender_id = text_data_json['from']
            receiver_id = text_data_json['to']
            await self.read_notification(sender_id, receiver_id)
        else:
            message = text_data_json['message']
            now = timezone.now()

            sender_id = text_data_json['sender']
            receiver_id = text_data_json['receiver']

            await self.save_message(self.user.username, self.room_group_name, message)
            await self.send_notification(sender_id, receiver_id)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.user.username,
                    'datetime': now.isoformat(),
                    'sender_id': sender_id,
                    'receiver_id': receiver_id
                }
            )

    # Receive message from room group
    async def chat_message(self, event):

        message = event['message']
        user = event['user']
        datetime = event['datetime']
        receiver_id = event['receiver_id']
        sender_id = event['sender_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'datetime': datetime,
            'sender_id': sender_id,
            'receiver_id': receiver_id
        }))

    @database_sync_to_async
    def save_message(self, username, thread_name, content):
        ChatMessage.create(username, content, thread_name)

    @database_sync_to_async
    def send_notification(self, sender, receiver):
        if Notification.objects.filter(sender_id=sender, receiver_id=receiver).exists():
            Notification.mark_as_not_seen(sender, receiver)
        else:
            Notification.create(sender, receiver)

    @database_sync_to_async
    def read_notification(self, sender, receiver):
        Notification.mark_as_seen(sender, receiver)
