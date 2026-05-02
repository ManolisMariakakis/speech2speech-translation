# Speech2Speech Translation (Greek → English)

Real-time speech translation system that converts spoken Greek into English text and audio.

## 🚀 Features

- 🎙️ Live Greek speech input (microphone)
- 🌍 Real-time translation to English
- 🔊 Audio playback for listeners (Text-to-Speech)
- ⚡ Low-latency streaming using WebSockets
- 🧠 Powered by Whisper (faster-whisper via whisper-live)

## 🏗️ Architecture

Speaker → Whisper (translation) → Relay (WebSocket) → Listener

- **Speaker** captures microphone audio and streams it
- **whisper-live** performs real-time Greek → English translation
- **Relay server** broadcasts messages to all connected clients
- **Listener** receives text and plays audio via browser TTS

## 🛠️ Tech Stack

- whisper-live (real-time ASR + translation)
- faster-whisper (Whisper inference)
- Python WebSocket relay (websockets)
- Browser Audio API (Web Audio / PCM streaming)
- Browser SpeechSynthesis (TTS)

## 📦 Use Cases

- Church live translation
- Conferences & talks
- Real-time interpretation
- Accessibility for multilingual audiences
