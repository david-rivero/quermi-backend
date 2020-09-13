# https://getstream.io/chat/react-native-chat/tutorial/
# Chat messages handle in frontend
# Get from backend tokens needed

from datetime import datetime
import json
import os
import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.conf.urls import url

import redis

MAX_NUMBER = 230102913
MIN_NUMBER = 22391
LIMIT_MESSAGES = 50
r = redis.Redis(
    charset='utf-8', decode_responses=True)


class DumbMessageModel:
    @staticmethod
    def init_chat(from_profile, to_profile):
        if not r.get('chat_{}_{}'.format(from_profile, to_profile)):
            ran_num = random.randint(MIN_NUMBER, MAX_NUMBER)
            value = 'chat_room_{}'.format(ran_num)
            r.set('chat_{}_{}'.format(from_profile, to_profile), value)
            r.set('chat_{}_{}'.format(to_profile, from_profile), value)
        return r.get('chat_{}_{}'.format(from_profile, to_profile))

    @staticmethod
    def save_message(message, from_profile, to_profile):
        ts_message = int(datetime.now().timestamp())
        key_message = 'chat_{}_{}_message_{}'.format(
            from_profile, to_profile, ts_message)
        r.set(key_message, message)

    # TODO: Perform this operation
    @staticmethod
    def retrieve_last_messages_from_profile(from_profile, to_profile):
        last_messages = []
        pattern_st = 'chat_{from_p}_{to_p}_message*'.format(
            from_p=from_profile,
            to_p=to_profile
        )
        pattern_nd = 'chat_{to_p}_{from_p}_message*'.format(
            from_p=from_profile,
            to_p=to_profile
        )
        keys_st = r.keys(pattern=pattern_st)
        keys_nd = r.keys(pattern=pattern_nd)
        total_keys = (keys_st + keys_nd)
        total_keys.sort(
            key=lambda row: int(row.split('_').pop()))

        for key in total_keys:
            message = r.get(key)
            last_messages.append(message)
            if len(last_messages) == LIMIT_MESSAGES:
                return last_messages

        return last_messages


class ChatConsumer(AsyncWebsocketConsumer):
    async def fetch_messages(self, _):
        last_messages = DumbMessageModel.retrieve_last_messages_from_profile(
            self.from_profile, self.to_profile)
        for message in last_messages:
            await self.send_message(message)

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_{}'.format(self.room_id)
        self.from_profile = self.scope['url_route']['kwargs']['from']
        self.to_profile = self.scope['url_route']['kwargs']['to']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data.get('message') or None)

    async def new_message(self, message):
        DumbMessageModel.save_message(
            message, self.from_profile, self.to_profile)
        self.send_chat_message(message)

    # Receive message from room group
    def send_message(self, message):
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    # Receive message from WebSocket
    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

websocket_urlpatterns = [
    url(r'ws/chat/(?P<room_id>.*)/(?P<from>\w+)/(?P<to>\w+)/$',
        ChatConsumer),
]
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})