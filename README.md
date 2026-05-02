# Speech2Speech Translation (Greek → English)

Real-time speech translation system that converts **spoken Greek into English text and audio**, designed for live environments such as churches, conferences, and events.

---

## Features

- Live microphone input (Greek speech)
- Real-time translation to English
- Low-latency streaming
- Audio playback via browser Text-to-Speech (TTS)
- Powered by Whisper (faster-whisper via whisper-live)
- WebSocket-based broadcast to multiple listeners

---

## Architecture

Speaker → Whisper (translation) → Relay (WebSocket) → Listener

### Components

- **Speaker (browser)**  
  Captures microphone audio and streams it to Whisper

- **whisper-live (server)**  
  Performs real-time Greek → English translation

- **Relay server (Python WebSocket)**  
  Broadcasts translated text to all connected listeners

- **Listener (browser)**  
  Receives translation and plays audio via TTS

---

## Tech Stack

- Python
- whisper-live
- faster-whisper (OpenAI Whisper inference)
- websockets (Python)
- Web Audio API (PCM streaming)
- Browser SpeechSynthesis API (TTS)

---

## Installation

### 1. Clone repository

```bash
cd ~
git clone https://github.com/ManolisMariakakis/speech2speech-translation.git
cd speech2speech-translation
```

---

### 2. Install dependencies

```bash
pip install faster-whisper websockets hf_transfer
```

---

### 3. Clone whisper-live

```bash
cd ~
git clone https://github.com/collabora/whisper-live.git
cd whisper-live

pip install -r rcd ~equirements/server.txt
```

---

## Run the system

### 1. Start Whisper server

```bash
cd ~/whisper-live

python run_server.py   --port 8000   --backend faster_whisper   --no_single_model   --raw_pcm_input   --max_connection_time 86400
```

---

### 2. Start Relay server

```bash
cd ~/speech2speech-translation
python relay.py
```

---

### 3. Start Web UI

```bash
cd ~/speech2speech-translation/speech2speech
python3 -m http.server 8080
```

---

## Usage

### Speaker

Open:

http://localhost:8080/speaker.html

- Click **Start**
- Speak Greek
- Translation is sent in real-time

---

### Listener

Open:

http://localhost:8080/listener.html

- Click **Connect Audio**
- Hear English translation

---

## Configuration

### Model selection (Speaker UI)

- `small` → fast, lower accuracy  
- `medium` → best balance (recommended)  
- `large-v3` → highest accuracy, higher latency  

---

## Use Cases

- ⛪ Church live translation
- 🎤 Conferences & talks
- 🌍 Multilingual accessibility
- 🎧 Real-time interpretation

---

## Notes

- Works best with clear audio input
- Requires modern browser (Chrome recommended)
- TTS quality depends on browser voice engine

---

## Future Improvements

- External TTS (OpenAI / ElevenLabs)
- Mobile optimization
- Multi-language support
- Docker deployment
- Cloud deployment (RunPod / GPU servers)

---

## License

MIT License

---
