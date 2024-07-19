import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'video_call_{self.room_name}'

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

    # Receive WebSocket messages from the user
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        if action == 'offer':
            offer = text_data_json['offer']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'offer',
                    'offer': offer
                }
            )
        elif action == 'answer':
            answer = text_data_json['answer']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'answer',
                    'answer': answer
                }
            )
        elif action == 'ice':
            ice = text_data_json['ice']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ice',
                    'ice': ice
                }
            )

    # Receive message from room group
    async def offer(self, event):
        offer = event['offer']
        await self.send(text_data=json.dumps({
            'action': 'offer',
            'offer': offer
        }))

    async def answer(self, event):
        answer = event['answer']
        await self.send(text_data=json.dumps({
            'action': 'answer',
            'answer': answer
        }))

    async def ice(self, event):
        ice = event['ice']
        await self.send(text_data=json.dumps({
            'action': 'ice',
            'ice': ice
        }))
