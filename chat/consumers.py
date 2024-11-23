import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'
            
            logger.info(f"Attempting to connect to room: {self.room_name}")

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            logger.info(f"Successfully connected to room: {self.room_name}")
            
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}")
            raise

    async def disconnect(self, close_code):
        try:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"Disconnected from room: {self.room_name} with code: {close_code}")
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}")
        finally:
            raise StopConsumer()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            username = text_data_json['username']

            logger.info(f"Received message from {username} in room {self.room_name}")

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )
        except Exception as e:
            logger.error(f"Error in receive: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'Failed to process message'
            }))

    async def chat_message(self, event):
        try:
            message = event['message']
            username = event['username']

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'username': username
            }))
            logger.info(f"Sent message to {self.channel_name} in room {self.room_name}")
        except Exception as e:
            logger.error(f"Error in chat_message: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'Failed to send message'
            }))
