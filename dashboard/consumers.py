import json
from channels.generic.websocket import AsyncWebsocketConsumer
class DashboardConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    print('connect....')
    await self.accept()
    await self.send(text_data=json.dumps({"message": 'connected...'}))
    self.room_group_name = 'sensor_temperature'
    # Join room group
    await self.channel_layer.group_add(self.room_group_name, self.channel_name)

  # Receive message from group
async def sensor_temperature(self, event):
    message = event["message"]
    # Send message to WebSocket
    await self.send(text_data=json.dumps({"message": message['payload']}))