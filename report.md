
----------
## REPORT.md
----------

## System Overview

This project implements a voice-driven coding pipeline that connects wake-word detection, local speech recognition, and an AI coding agent (Aider) to enable near hands-free programming.

Pipeline:

Wake Word → Audio Capture → Whisper STT → Confirmation Layer → Aider CLI → Git Commit

---

## Wake Word System

OpenWakeWord was used for activation via "Hey Jarvis".


- Runs locally using ONNX
- Tuned threshold to 0.9 to reduce false positives
- Added cooldown period to prevent retriggering during execution

Trade-off: Higher threshold reduced false triggers but slightly increased activation strictness.

---

## Speech-to-Text (Whisper)

Local Whisper (`base` model) was selected instead of cloud APIs.

Reasons:
- Privacy (avoids sending code-related audio externally)
- Cost reduction (~$0.006/min avoided cloud STT usage)
- Acceptable latency (~2s for 5s audio clip)

Trade-offs:
- Occasional misinterpretation of technical terms
- Heavier than `tiny`, slower than cloud APIs

---

## Confirmation System

A hybrid safety mechanism was implemented:

- 15-second auto-accept timeout
- Manual controls:
  - Space → accept
  - R → re-record

Reasoning: Fully hands-free execution was avoided due to risk of transcription errors leading to destructive commands.

Trade-off: Not 100% voice-only, but significantly safer in real-world usage.

---

## Aider Integration

Aider was chosen due to:

- Native CLI support (`--message`, `--yes`)
- Easy subprocess automation
- Stable model integration with Groq

LLM backend: Groq Llama 3.3 70B

Benefits:
- Fast response time (3–8 seconds typical)
- No cost per request compared to OpenAI GPT-4

---

## Git Automation

After each execution:
- `git add .`
- `git commit -m "<prompt>"`

This creates:
- Full audit trail of voice-driven changes
- Easy rollback system for unsafe modifications

---

