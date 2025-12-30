import os
import datetime
import json
import requests
from confluent_kafka import Consumer
import google.generativeai as genai

# 1. CONFIGURARE API KEYS
GEMINI_API_KEY = "GEMINI_API_KEY" 
ELEVEN_API_KEY = "ELEVENLABS_API_KEY"
VOICE_ID = "nPczCjzI2devNBz1zQrb"

genai.configure(api_key=GEMINI_API_KEY)

# 2. CONFIGURARE CONFLUENT KAFKA
conf = {
    'bootstrap.servers': 'CONFLUENT ADDRESS',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'API_KEY_ID',      
    'sasl.password': 'API_SECRET_CONFLUENT',   
    'group.id': 'smart_city_ai_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['date_hackathon'])

print("--- 🧠 AI Smart City Orchestrator: ONLINE (STABLE MODE) ---")
print("Waiting for sensor data from Confluent...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"❌ Kafka Error: {msg.error()}")
            continue

        # Citire mesaj de la Producer
        raw_data = msg.value().decode('utf-8')
        event = json.loads(raw_data)

        # --- REPARARE: Extragere sigură a datelor (fără KeyError) ---
        event_type = event.get('type', 'Emergency')
        location = event.get('location', 'Unspecified Location')
        detail = event.get('detail', 'General alert: response needed')

        print(f"\n📥 [NEW EVENT]: {event_type} at {location}")

        # 3. GEMINI - GENERARE PLAN
        print("🤖 AI is thinking...")
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # --- REPARARE: Folosim variabilele sigure în prompt ---
        prompt = f"Emergency type {event_type} at {location}: {detail}. Provide a 3-step action plan, max 30 words."
        
        try:
            response = model.generate_content(prompt)
            action_plan = response.text
            print(f"⚡ [AI PLAN]: {action_plan}")

            # 4. ELEVENLABS - GENERARE VOCE
            print("🎙️ Generating Voice via API...")
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVEN_API_KEY
            }
            
            data = {
                "text": action_plan,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            }

            res = requests.post(url, json=data, headers=headers)
            
            if res.status_code == 200:
                timestamp = datetime.datetime.now().strftime("%H%M%S")
                filename = f"voice_plan_{timestamp}.mp3"
                
                with open(filename, "wb") as f:
                    f.write(res.content)
                
                print(f"✅ SUCCESS: File saved as {filename}")
            else:
                print(f"❌ ELEVENLABS API ERROR: {res.status_code} - {res.text}")

        except Exception as e:
            print(f"❌ ERROR DURING PROCESSING: {e}")

except KeyboardInterrupt:
    print("\nStopping...")
finally:
    consumer.close()
