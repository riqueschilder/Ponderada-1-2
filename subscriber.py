import pytest
import paho.mqtt.client as mqtt
import time
import json

broker_address = "6f653f6202264f9293d430ac29f36a30.s1.eu.hivemq.cloud"
broker_port = 8883 
topic = "sensor/sps30"
mqtt_username = "riqueschilder"
mqtt_password = "Riqueschilder123"


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,reconnect_on_failure=True, client_id="riqueschilder-pytest")
        self.client.username_pw_set(mqtt_username, mqtt_password)
        self.client.tls_set()
        self.received_messages = []
        self.start_time = time.time()

    def on_connect(self, mqttc, obj, flags, reason_code, properties):
        print("Connected with result code")
        self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        self.received_messages.append((msg.payload, time.time()))

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_address, broker_port, 60)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

@pytest.fixture
def mqtt_client():
    client = MQTTClient()
    client.connect()
    yield client
    client.disconnect()

def test_recebimento(mqtt_client):
    time.sleep(3)
    assert len(mqtt_client.received_messages) > 0, "Nenhuma mensagem recebida"

def test_validacao_dos_dados(mqtt_client):
    time.sleep(5) 
    for payload, _ in mqtt_client.received_messages:
        data = json.loads(payload)
        assert all(key in data for key in ["mc_pm1_0", "mc_pm2_5", "mc_pm4_0", "mc_pm10"]), "Dados inválidos"

def test_confirmacao_da_taxa_de_disparo(mqtt_client):
    time.sleep(10)
    timestamps = [timestamp for _, timestamp in mqtt_client.received_messages]
    deltas = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
    assert all(1.5 <= delta <= 2.5 for delta in deltas), "Taxa de recebimento inconsistente"
