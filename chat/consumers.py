from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.dispatch.dispatcher import receiver

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'welcome',
                'tester': 'welcome to the WEBCHAT',
            }
        )
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def welcome(self,event):
        tester = event['tester']
        await self.send(text_data=json.dumps({
            'tester' : tester,
        }))

    async def receive(self, text_data):
        text_datas = json.loads(text_data)
        message = text_datas['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
            }
        )

    async def chat_message(self,event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message' : message,
        }))
        
        #return await super().receive(text_data=text_data, bytes_data=bytes_data)
    #pass