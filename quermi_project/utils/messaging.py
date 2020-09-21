# https://getstream.io/chat/react-native-chat/tutorial/
# Chat messages handle in frontend
# Get from backend tokens needed

from datetime import datetime
import json
import os
import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.conf.urls import url

import redis

MAX_NUMBER = 230102913
MIN_NUMBER = 22391
LIMIT_MESSAGES = 50
r = redis.Redis(
    charset='utf-8', decode_responses=True)
automatic_response = {
    'Hi': 'Hello',
    'How are you': 'I\'m fine, thanks',
    'Are you available': 'Yes, I\'m available that day',
    'Bye': 'bye',
    '__default__': 'Sorry, I cannot understand your message.'
}

class DumbMessageModel:
    @staticmethod
    def get_automatic_response(message):
        resp_keys = list(automatic_response.keys())
        for k in resp_keys:
            if message.lower().find(k.lower()) != -1:
                return automatic_response[k]
        return automatic_response['__default__']


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
            formatted_key = key.replace(
                'chat_', '').replace('message_', '')
            from_prof, to_prof, ts_ms = formatted_key.split('_')
            last_messages.append({
                'message': message,
                'from_profile': from_prof,
                'to_profile': to_prof,
                'ts_message': ts_ms
            })
            if len(last_messages) == LIMIT_MESSAGES:
                return last_messages

        return last_messages


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, _):
        last_messages = DumbMessageModel.retrieve_last_messages_from_profile(
            self.from_profile, self.to_profile)
        for message in last_messages:
            self.send_message(message)

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_{}'.format(self.room_id)
        self.from_profile = self.scope['url_route']['kwargs']['from']
        self.to_profile = self.scope['url_route']['kwargs']['to']
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        self.commands = {
            'fetch_messages': self.fetch_messages,
            'new_message': self.new_message
        }
        data = json.loads(text_data)
        self.commands[data['command']](data.get('message') or None)

    def new_message(self, message):
        DumbMessageModel.save_message(
            message, self.from_profile, self.to_profile)

        # TODO: Update automatic response behavior
        response_message = DumbMessageModel.get_automatic_response(message)
        self.send_chat_message(response_message)
        DumbMessageModel.save_message(
            response_message, self.to_profile, self.from_profile)

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
                'type': 'send_message',
                'message': message
            }
        )


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