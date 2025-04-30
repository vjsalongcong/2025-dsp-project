
from datetime import datetime
from flask import Flask, jsonify
from flask_socketio import SocketIO
import random
import threading
from flask_cors import CORS
from scd4x import SCD4X
from paho.mqtt import client as mqtt_client
import json

# Load configuration from config.json
try:
    with open("config.json", "r") as f:
        # Load and Cache config
        config = json.load(f)
        
        # Define config sections
        calibration = config["calibration"]
        thresholds = config["thresholds"]
        mqtt = config["mqtt"]
        
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Config error: {e}")
    exit(1)

class SensorDataCache:
    def __init__(self):
        # Initialise temporary data
        self.data = {"co2": "...", "temperature": "...", "humidity": "...", "iaq_health": "good", "timestamp": datetime.now()}
        self.lock = threading.Lock()

    def update(self, data_payload):
        # Update cached data
        with self.lock:
            self.data = data_payload

    def get(self):
        # Retrieve cached data
        with self.lock:
            return self.data.copy()

class SensorReader:
    def __init__(self):
        # Initialise SCD41 sensor
        self.device = SCD4X(quiet=False)
        self.device.start_periodic_measurement()

    def read(self):
        # Read data
        co2, temperature, humidity, timestamp = self.device.measure()
        
        # Calibrate data with config
        co2 = max(0, co2 + calibration["carbon_dioxide"])
        temperature = max(0, temperature + calibration["temperature"])
        humidity = min(100, max(0, humidity + calibration["humidity"]))
        
        # Determine IAQ health with config
        temp_good = thresholds["min-temperature"] <= temperature <= thresholds["max-temperature"]
        humidity_good = thresholds["min-humidity"] <= humidity <= thresholds["max-humidity"]
        co2_good = co2 <= thresholds["carbon_dioxide"]
        
        if temp_good and humidity_good and co2_good:
            iaq_health = "good"
        else:
            iaq_health = "bad"
        
        # Return data
        return co2, temperature, humidity, iaq_health, datetime.now()
    
class MQTTClientHandler:
    def __init__(self):
        # Initialise MQTT details
        self.broker = mqtt["broker"]
        self.port = mqtt["port"]
        self.topic = mqtt["topic"]
        self.client_id = f'raspberrypi-{random.randint(0, 1000)}'
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, self.client_id)
        
        # Attempt to connect
        try:
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
            print("MQTT: Connection to broker established")
            self.established = True
        except:
            print("MQTT: There was an error establishing connection")
            self.established = False
            

    def publish(self, message):
        # Publish data
        if self.established == True:
            self.client.publish(self.topic, json.dumps(message))

class SensorService(threading.Thread):
    def __init__(self, sensor_reader, data_cache, mqtt_handler, socketio):
        # Initialise threads
        super().__init__()
        self.sensor_reader = sensor_reader
        self.data_cache = data_cache
        self.mqtt_handler = mqtt_handler
        self.socketio = socketio
        self.daemon = True

    def run(self):
        while True:
            # Read sensor data
            co2, temp, humidity, iaq_health, timestamp = self.sensor_reader.read()
            
            # Create data payload
            data_payload = {
                "co2": co2,
                "temperature": round(temp, 1),
                "humidity": round(humidity, 1),
                "iaq_health": iaq_health,
                "timestamp": timestamp.isoformat()
            }
            
            # Export data payload
            self.data_cache.update(data_payload)
            self.socketio.emit('sensor_update', data_payload)
            self.mqtt_handler.publish(data_payload)

# Flask App Setup
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Create instances
data_cache = SensorDataCache()
sensor_reader = SensorReader()
mqtt_handler = MQTTClientHandler()
sensor_service = SensorService(sensor_reader, data_cache, mqtt_handler, socketio)

@app.route('/')
def index():
    return "Flask server is running"

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    return jsonify(data_cache.get())

if __name__ == '__main__':
    sensor_service.start()
    socketio.run(app, host='0.0.0.0', port=5500)
