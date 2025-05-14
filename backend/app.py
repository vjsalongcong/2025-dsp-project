
from datetime import datetime
from flask import Flask, jsonify, request
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
        # Initialise MQTT state
        self.established = False
        self.client = None
        self.update_config(mqtt)
            
    def update_config(self, config_mqtt):
        # Check if client is connected
        if self.client:
            try:
                self.client.loop_stop()
                self.client.disconnect()
                print("MQTT: Existing connection stopped")
            except Exception as e:
                print(f"MQTT: Error disconnecting previous client - {e}")
                
        # Initialise MQTT details
        self.broker = config_mqtt["broker"]
        self.port = config_mqtt["port"]
        self.topic = config_mqtt["topic"]
        self.client_id = f'raspberrypi-{random.randint(0, 1000)}'
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, self.client_id)
        
        # Attempt to connect
        try:
            self.client.username_pw_set(config_mqtt["username"], config_mqtt["password"])
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

# Index page to see if Flask is running
@app.route('/')
def index():
    return "Flask server is running"

# Route to retrieve cached sensor data
@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    return jsonify(data_cache.get())

# Route to retrieve calibration settings
@app.route('/api/iaq-calibration', methods=['GET', 'POST'])
def settings_iaq_calibration():
    global config, calibration
    
    if request.method == 'GET':
        # Create data payload
        data_payload = {
            "temperature": calibration["temperature"],
            "humidity": calibration["humidity"],
            "carbon_dioxide": calibration["carbon_dioxide"],
            "carbon_monoxide": calibration["carbon_monoxide"],
            "nitrogen_dioxide": calibration["nitrogen_dioxide"],
            "ammonia": calibration["ammonia"]
        }

        # Return requested data
        return jsonify(data_payload)
    
    if request.method == 'POST':
        # Retrieve request
        data = request.get_json()
        
        # Attempt to update data
        try:
            # Save data to config.json
            config['calibration'] = data
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            
            # Re-read calibration section
            with open("config.json", "r") as f:
                config = json.load(f)
                calibration = config["calibration"]
                
            return jsonify({'status': 'success'})
        except:
            return jsonify({'status': 'error'}), 400

# Route to retrieve threshold settings
@app.route('/api/iaq-threshold', methods=['GET', 'POST'])
def settings_iaq_threshold():
    global config, thresholds
    
    if request.method == 'GET':
        # Create data payload
        data_payload = {
            "max-temperature": thresholds["max-temperature"],
            "min-temperature": thresholds["min-temperature"],
            "max-humidity": thresholds["max-humidity"],
            "min-humidity": thresholds["min-humidity"],
            "carbon_dioxide": thresholds["carbon_dioxide"],
            "carbon_monoxide": thresholds["carbon_monoxide"],
            "nitrogen_dioxide": thresholds["nitrogen_dioxide"],
            "ammonia": thresholds["ammonia"]
        }

        # Return requested data
        return jsonify(data_payload)
    
    if request.method == 'POST':
        # Retrieve request
        data = request.get_json()
        
        # Attempt to update data
        try:
            # Save data to config.json
            config['thresholds'] = data
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            
            # Re-read thresholds section
            with open("config.json", "r") as f:
                config = json.load(f)
                thresholds = config["thresholds"]
                
            return jsonify({'status': 'success'})
        except:
            return jsonify({'status': 'error'}), 400

# Route to retrieve threshold settings
@app.route('/api/mqtt', methods=['GET', 'POST'])
def settings_mqtt():
    global config, mqtt
    
    if request.method == 'GET':
        # Create data payload
        data_payload = {
            "broker": mqtt["broker"],
            "port": mqtt["port"],
            "topic": mqtt["topic"],
            "username": mqtt["username"],
            "password": ""
        }
        
        # Return requested data
        return jsonify(data_payload)
    
    if request.method == 'POST':
        # Retrieve request
        data = request.get_json()
        
        # Attempt to update data
        try:
            # Save data to config.json
            config['mqtt'] = data
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            
            # Re-read mqtt section
            with open("config.json", "r") as f:
                config = json.load(f)
                mqtt = config["mqtt"]
            
            # Reconnect mqtt
            mqtt_handler.update_config(mqtt)
                
            return jsonify({'status': 'success'})
        except:
            return jsonify({'status': 'error'}), 400

if __name__ == '__main__':
    sensor_service.start()
    socketio.run(app, host='0.0.0.0', port=5500, allow_unsafe_werkzeug=True)
