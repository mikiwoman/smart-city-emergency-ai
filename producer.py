import time
import json
from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'ADRESA_TA_CONFLUENT', 
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'API_KEY_ID',
    'sasl.password': 'API_SECRET_CONFLUENT'
}

producer = Producer(conf)
topic = 'date_hackathon'

city_events = [
    {"sensor_id": "CAM-001", "type": "EMERGENCY", "location": "Main St & 5th Ave", "detail": "Ambulance approaching - clear intersection"},
    {"sensor_id": "SENS-102", "type": "TRAFFIC", "location": "Downtown Bridge", "detail": "Heavy congestion - average speed 5km/h"},
    {"sensor_id": "CAM-005", "type": "ACCIDENT", "location": "Highway Exit 12", "detail": "Two-car collision - blocking left lane"},
    {"sensor_id": "SENS-088", "type": "CROWD", "location": "City Hall Square", "detail": "Protest gathering - 500+ people on roadway"},
    {"sensor_id": "GRID-01", "type": "INFRASTRUCTURE", "location": "Sector 4", "detail": "Power outage - street lights offline"},
    {"sensor_id": "WEA-04", "type": "WEATHER", "location": "North Underpass", "detail": "Flash flooding - water level 30cm"},
    {"sensor_id": "CAM-012", "type": "HAZARD", "location": "Industrial Zone", "detail": "Large debris fallen on roadway"},
    {"sensor_id": "SENS-201", "type": "FIRE", "location": "Grand Hotel", "detail": "Building fire - smoke obstructing visibility"},
    {"sensor_id": "CAM-020", "type": "VANDALISM", "location": "Central Park", "detail": "Smart pole damaged - Wi-Fi hub offline"},
    {"sensor_id": "SENS-300", "type": "VIP_ESCORT", "location": "Airport Road", "detail": "Diplomatic convoy - secure corridor needed"}
]

def delivery_report(err, msg):
    """ Raport de livrare a mesajului către Kafka """
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Event sent to {msg.topic()} [{msg.partition()}]")

print("--- 🚀 SMART CITY SENSOR SIMULATOR: STARTING ---")

for event in city_events:
    
    message_value = json.dumps(event)
    
    print(f"Sending: {event['type']} at {event['location']}...")
    
    producer.produce(topic, value=message_value, callback=delivery_report)
    
    producer.flush()
    
    time.sleep(4) 

print("--- ✅ ALL 10 EVENTS PROCESSED ---")
