# import json
#
# from channels.generic.websocket import WebsocketConsumer
#
#
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data, **kwargs):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#
#         self.send(text_data=json.dumps({"message": message}))

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# #Синхронный потребитель
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"



        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": f'юзер: {message}'}))

    # Receive question from taskmaster
    def question(self, event):
        question = event["question"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"question": question}))






# import json

# from channels.generic.websocket import AsyncWebsocketConsumer


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"
#         self.username = self.scope['user']
#
#         # Join room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat.message", "message": message}
#         )
#
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": f'{self.username}: {message}'}))
#
#
#     async def quiz_monitor(self, event):
#         question = event['question']
#         await self.send(text_data=json.dumps({'question': f'Вопрос №{0}:{question}'}))
