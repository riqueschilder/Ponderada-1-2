import paho.mqtt.client as mqtt
import time
import struct
import json
import random

broker_address = "6f653f6202264f9293d430ac29f36a30.s1.eu.hivemq.cloud"
broker_port = 8883 

mqtt_username = "riqueschilder"
mqtt_password = "Riqueschilder123"

topic = "sensor/sps30"

def simulate_sps30_data():
    data = {
        "mc_pm1_0": struct.pack(">I", random.randint(0, 100)),
        "mc_pm2_5": struct.pack(">I", random.randint(0, 100)),
        "mc_pm4_0": struct.pack(">I", random.randint(0, 100)),
        "mc_pm10": struct.pack(">I", random.randint(0, 100)),
    }
    hex_data = {k: v.hex() for k, v in data.items()}
    return json.dumps(hex_data)

def on_connect(mqttc, obj, flags, reason_code, properties):
    print(f"Connected with reason code: {reason_code}\n")

def on_publish(mqttc, obj, mid, reason_code, properties):
    print(f"Message ID: {mid} published")

def on_message(mqttc, obj, msg):
    print(f"{msg.topic} {msg.qos} {msg.payload}")

client = mqtt.Client(protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

client.username_pw_set(mqtt_username, mqtt_password)

client.tls_set() 
client.connect(broker_address, broker_port, 60)

client.loop_start()

print("Connecting to broker...")

try:
    while True:
        sensor_data = simulate_sps30_data()
        info = client.publish(topic, sensor_data, qos=1)
        info.wait_for_publish()
        print(f"Sent on topic: {topic}")
        print(f"{sensor_data}\n")
        time.sleep(2)

except KeyboardInterrupt:
    client.disconnect()
    print("Simulation stopped")
