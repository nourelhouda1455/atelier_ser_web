from mqttasgi.consumers import MqttConsumer

from persistence.persistence_engine import persist_mesure, persist_to_firebase

class MqttTopicsConsumer(MqttConsumer):

    async def connect(self):
        print("Connecting to MQTT broker...")
        try:
            await self.subscribe("sensor/temperature",0)
        except Exception as e:
            print(f"Error occurred while subscribing to topic: {e}")
        print("Subscribed to topic: sensor/temperature")
        self.room_group_name = 'sensor_temperature'
        # Join room group
        try:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        except Exception as e:
            print(f"Error occurred while joining room group: {e}")

    async def receive(self, mqtt_message):
        print(f"Received MQTT message at topic: {mqtt_message['topic']}")
        print(f"Message payload: {mqtt_message['payload'].decode()}")
        print(f"QoS level: {mqtt_message['qos']}")
        # persist the message to the database
        await persist_mesure(mqtt_message['payload'].decode("utf-8"))
        await persist_to_firebase(mqtt_message['payload'].decode("utf-8"))
        # Send message to room group
        try:
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "sensor.temperature",
                "message": {"payload": mqtt_message['payload'].decode("utf-8")}
            }
        )
        except Exception as e:
            print(f"Error occurred while sending message to room group: {e}")

    async def disconnect(self):
        await self.unsubscribe('sensor/temperature')

    #Receive message from group
    async def sensor_temperature(self, event):
        print(f"Received message from group: {event['message']}")
        message = event["message"]
        # push message to database
        #persistData(message['payload'])

    
        
              