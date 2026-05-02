# Speaker.html — Step-by-Step Explanation (Greek → English Realtime)

## Overview

`speaker.html` is the **speaker-side web interface**.
It captures audio from the microphone, sends it to a Whisper server (`whisper-live` on port `8000`), receives translated English text, and forwards stable segments to a relay server (`relay.py` on port `9001`) for listeners.

---

## 1. User Interface (HTML)

The page includes:

* **Start / Stop buttons**
* **Model selector** (small, medium, large-v3)
* **Status + error display**
* **Three text panels**

### Panels

| Panel                   | Purpose                                     |
| ----------------------- | ------------------------------------------- |
| Current Whisper Text    | Live transcription/translation from Whisper |
| Pending Stable Segments | Segments waiting to be confirmed as stable  |
| Sent to Listener        | Final text already sent to listeners        |

---

## 2. Core Connections

Three main connections are used:

```text
whisperWs → Whisper server (port 8000)
relayWs   → Relay server (port 9001)
HTTP      → Web server (port 8080)
```

### Description

* **Whisper WebSocket (8000)**
  Sends microphone audio and receives real-time transcription/translation.

* **Relay WebSocket (9001)**
  Forwards processed (stable) translated text to listeners.

* **Web Server (8080)**
  Hosts the `speaker.html` page (and optionally `listener.html`) via a simple HTTP server (e.g. `python -m http.server 8080`).

### Typical Run Setup

```bash
# Whisper server
python run_server.py --port 8000 ...

# Relay server
python relay.py  # (port 9001)

# Web server
python3 -m http.server 8080
```

This results in:

```text
http://localhost:8080/speaker.html
ws://localhost:8000
ws://localhost:9001
```

---

## 3. Text Processing

### Clean text

```js
cleanText()
```

* Removes extra spaces
* Fixes punctuation spacing

---

### Normalize text

```js
normalize()
```

* Lowercases
* Removes punctuation
* Used for comparison

---

### Similarity detection

```js
isSimilar(a, b)
```

Prevents duplicate or nearly identical sentences from being sent.

---

## 4. WebSocket URL Handling

```js
getWsUrl(port)
```

Supports both:

* Localhost
* RunPod proxy environments

Example:

```
xxxxx-8080.proxy.runpod.net → xxxxx-8000.proxy.runpod.net
```

---

## 5. Audio Processing Pipeline

### Step 1: Capture audio

```js
navigator.mediaDevices.getUserMedia()
```

---

### Step 2: Downsample

```js
downsampleBuffer()
```

Converts browser audio (44.1kHz / 48kHz) → **16kHz**

---

### Step 3: Convert to PCM

```js
floatTo16BitPCM()
```

Required for:

```
--raw_pcm_input (whisper-live)
```

---

### Step 4: Send audio

```js
whisperWs.send(pcm)
```

---

## 6. Handling Whisper Output

### Case A: Segment-based output

```js
data.segments
```

* Updates **Current Text**
* Only processes segments where:

```js
segment.completed === true
or
segment.final === true
```

---

### Case B: Plain text fallback

If no segments exist:

* Sends text only if:

  * Ends with punctuation (`. ! ?`)
  * OR has ≥ 10 words

---

## 7. Pending Segments Logic

```js
addPendingSegment()
```

Segments are **not sent immediately**.

Instead:

1. Stored in `pendingSegments`
2. Wait for stability (1.2 seconds)

---

### Delay system

```js
COMMIT_DELAY_MS = 1200
```

Handled by:

```js
scheduleCommit()
commitReadySegments()
```

---

## 8. Sending Final Text

```js
commitSegment()
```

Checks:

* Not already sent
* Not similar to previous

Then sends:

```js
sendToRelay(text)
```

---

### Payload format

```json
{
  "type": "translation",
  "text": "The Lord is my shepherd.",
  "lang": "en",
  "ts": 1710000000000
}
```

---

### Queue system

If relay is not ready:

```js
relayQueue.push(payload)
```

Later:

```js
flushRelayQueue()
```

---

## 9. Relay Connection

```js
connectRelay()
```

Features:

* Auto reconnect
* Queue flushing
* Error handling

---

## 10. Start Flow

```js
start()
```

Steps:

1. Reset UI and buffers
2. Request microphone access
3. Connect to relay
4. Connect to Whisper
5. Send configuration:

```json
{
  "uid": "speaker-...",
  "language": "el",
  "task": "translate",
  "model": "large-v3",
  "use_vad": true
}
```

6. Start streaming audio

---

## 11. Stop Flow

```js
stop()
```

Stops everything:

* Audio processing
* Microphone stream
* Whisper connection
* Relay connection

---

## 12. Full Data Flow

```
Microphone
   ↓
AudioContext
   ↓
Downsample (→ 16kHz)
   ↓
16-bit PCM
   ↓
WebSocket → Whisper (8000)
   ↓
Greek → English translation
   ↓
Stable segment filtering
   ↓
Duplicate prevention
   ↓
WebSocket → Relay (9001)
   ↓
Listeners receive text
```

---

## Summary

`speaker.html` acts as a **real-time speech translation controller**:

* Captures Greek speech
* Sends audio to Whisper
* Receives translated English text
* Filters unstable/duplicate segments
* Sends only clean, stable output to listeners

It ensures:

* Smooth real-time experience
* No duplicated sentences
* Stable translation delivery

---
