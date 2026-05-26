# Voice Interface for Aider

A voice-driven coding assistant that converts speech commands into terminal-based AI code execution using Whisper STT, OpenWakeWord, Groq LLM, and Aider.

* Features

  * Wake word activation (“Hey Jarvis”) using OpenWakeWord (<100ms latency)
  * Local Whisper speech-to-text for privacy-preserving transcription
  * Confirmation system with 15s auto-accept + manual re-record option
  * Terminal-based AI coding via Aider + Groq LLM backend
  * Automatic git commits after each execution for full change history

* Tech Stack

  
  * Speech recognition – OpenAI Whisper 
  * LLM backend – Groq Cloud 
  * Coding agent – Aider (terminal AI assistant)
  * Version control – Git 
  * Wake word detection – OpenWakeWord with ONNX runtime 



* Installation (Windows)

  * Create virtual environment: `virtualenv venv`
  * Activate: `venv\Scripts\activate`
  * Install FFmpeg: `winget install ffmpeg`
  * Install dependencies: `pip install -r requirements.txt`
  * Set API key: `$env:GROQ_API_KEY="your_key_here"`

* How to Run

  * Run `python app.py`
  * Say "Hey Jarvis" and speak your coding request after the prompt


