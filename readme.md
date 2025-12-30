# 🌆 Smart City AI Emergency Orchestrator

This project is an automated emergency response system designed for future Smart Cities. It processes real-time sensor data, generates actionable response plans using AI, and converts them into voice commands for immediate broadcasting.

## 🚀 How it Works
1. **Data Ingestion**: Emergency events (Fire, Medical, Traffic, etc.) are streamed via **Confluent Kafka**.
2. **AI Orchestration**: **Google Gemini 1.5/2.0 Flash** analyzes the event and generates a concise, 3-step action plan in under 2 seconds.
3. **Voice Synthesis**: **ElevenLabs API** converts the text plan into a high-quality human voice (Brian) to be broadcasted to emergency units.

## 🛠️ Tech Stack
- **Streaming**: Confluent Cloud (Kafka)
- **AI Model**: Google Gemini 2.0 Flash / 1.5 Flash
- **Voice AI**: ElevenLabs (Multilingual v2)
- **Language**: Python 3.x

## 📋 Prerequisites
- Python 3.10+
- Confluent Cloud Account
- Google AI Studio API Key (Gemini)
- ElevenLabs API Key
