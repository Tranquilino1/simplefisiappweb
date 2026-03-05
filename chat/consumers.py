import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
import re

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from urllib.parse import unquote
        self.room_name = unquote(self.scope['url_route']['kwargs']['room_name'])
        
        # Limpiar caracteres ilegales para el group_name en Channels (solo alfa, digitos, guiones, puntos)
        safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', self.room_name)
        self.room_group_name = f'chat_{safe_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        # Determine if it's a normal chat message or WebRTC signal
        action_type = text_data_json.get('type', 'chat_message')
        
        username = self.scope['user'].username if self.scope['user'].is_authenticated else 'Anonymous'
        avatar_url = '/static/css/default_avatar.svg'
        if self.scope['user'].is_authenticated and hasattr(self.scope['user'], 'profile'):
            if self.scope['user'].profile.profile_picture:
                avatar_url = self.scope['user'].profile.profile_picture.url
                
        if action_type == 'chat_message':
            message = text_data_json['message']
            
            # Guardar el mensaje en BD si está autenticado
            if self.scope['user'].is_authenticated:
                await self.save_message(self.room_name, self.scope['user'], message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'avatar_url': avatar_url
                }
            )
        elif action_type == 'webrtc':
            # Signaling for WebRTC
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_signal',
                    'payload': text_data_json,
                    'sender': username
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event.get('username', 'Unknown')
        avatar_url = event.get('avatar_url', '/media/profiles/default.avif')
        msg_type = event.get('msg_type', 'text')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username,
            'avatar_url': avatar_url,
            'msg_type': msg_type
        }))

    async def webrtc_signal(self, event):
        # Forward WebRTC signal to WebSocket
        if event['sender'] != self.scope['user'].username:
            await self.send(text_data=json.dumps(event['payload']))

    @database_sync_to_async
    def save_message(self, room_name, user, message_content):
        room_obj, _ = Room.objects.get_or_create(name=room_name)
        Message.objects.create(room=room_obj, sender=user, content=message_content, msg_type='text')
