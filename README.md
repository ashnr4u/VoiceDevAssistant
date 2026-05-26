# Voice Interface for Aider

A voice-driven coding assistant that converts speech commands into terminal-based AI code execution using Whisper STT, OpenWakeWord, Groq LLM, and Aider.

---

## Features

- Wake word activation (“Hey Jarvis”) using OpenWakeWord (<100ms latency)
- Local Whisper speech-to-text for privacy-preserving transcription
- Confirmation system with 15s auto-accept + manual re-record option
- Terminal-based AI coding via Aider + Groq LLM backend
- Automatic git commits after each execution for full change history

---

## Installation (Windows)

```powershell
# Create virtual environment
virtualenv venv

# Activate environment
venv\Scripts\activate

# Install FFmpeg
winget install ffmpeg

# Install dependencies
pip install -r requirements.txt

# Set API key
$env:GROQ_API_KEY="your_key_here"

all set
run app.py-> say hey jarvis to activate and all