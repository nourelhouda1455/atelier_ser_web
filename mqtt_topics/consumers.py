import json
from mqttasgi.consumers import MqttConsumer
class MyMqttConsumer(MqttConsumer):
  async def connect(self):
    await self.subscribe('sensor/temperature', 2)

  async def receive(self, mqtt_message):
    print('Received a message at topic:', mqtt_message['topic'])
    print('With payload', mqtt_message['payload'])
    print('And QOS:', mqtt_message['qos'])

  async def disconnect(self):
   await self.unsubscribe('sensor/temperature')