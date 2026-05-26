REPORT.md – Voice Interface for Terminal Coding Agent (Aider)

1. Overview and Motivation

This project is a voice-driven interface for Aider, a terminal-based AI coding assistant. The goal is to let developers use voice to give coding commands instead of typing. The system listens for a wake word, records speech, transcribes it locally, confirms the command, runs it through Aider, and automatically commits changes with Git.

The main parts are:
- Wake word detection using OpenWakeWord ("Hey Jarvis")
- Audio recording with silence detection
- Local transcription using Whisper base model
- A 15-second auto-accept confirmation (with spacebar to accept or R to re-record)
- Aider execution with Groq Llama 3.3 70B
- Automatic Git commit after each run

2. Why Aider

I looked at three terminal coding agents: Aider, Pi, and OpenCode. Aider was the only one with a clean command-line interface that accepts a message directly without interactive prompts. The --message and --yes flags let me script it completely. Pi and OpenCode required hacking terminal sessions or lacked stable automation. Aider also auto-commits to Git, which gave me a free audit trail for voice changes.

3. Speech Recognition Choice – Local Whisper over Cloud APIs

I used Local Whisper won because of privacy and cost. Sending voice that might contain proprietary code to a cloud API is risky. Local runs offline and costs nothing. The trade-off is latency: about 2 seconds for a 5-second clip, and occasional mis-transcriptions of technical symbols like "->" becoming "to". But the confirmation step catches those errors.


4. Wake Word Engine – OpenWakeWord

OpenWakeWord runs fully offline with ONNX, has a pre-trained "Hey Jarvis" model, and reacts in under 100ms. The default threshold of 0.5 gave too many false positives from keyboard clicks and breathing. I raised it to 0.9, which almost eliminated false triggers but requires clearer speech. I also added a 3-second cooldown so the wake word doesn't fire again while Aider is running.

5. Confirmation – Why Not Fully Hands-Free

A fully hands-free system would execute after every transcription. That's dangerous because Whisper can make mistakes. One bad transcription could delete files. So I added a confirmation layer: the transcribed text is shown, and the system waits 15 seconds. If nothing happens, it auto-accepts. If the user hits spacebar, it accepts immediately. R key re-records.

The current design keeps the user mostly hands-free (auto-accept after 15 seconds) but gives a simple keyboard escape for safety.

6. LLM Backend – Groq Llama 3.3 70B

Groq is extremely fast, Local Llama on CPU is too slow (3-10 seconds) and would need a GPU for decent performance. The Groq free tier (30 requests per minute) is enough for development and demo. I set an environment variable for the API key and excluded it from the submission archive.

7. Integration with Aider

Aider runs as a subprocess. I capture its stdout and filter out noisy lines that mention tokens, cost, httpx, or litellm. Those logs are useful for debugging but clutter the terminal for a voice user. The user only sees the assistant's code output and error messages.

After Aider finishes, the script runs git add and git commit with the prompt as the commit message. This creates a full history of voice-driven changes. If something goes wrong, the user can revert with git reset.

If Aider takes longer than 120 seconds, the subprocess is terminated to avoid hanging. The user can then try again.

8. Limitations and Trade-offs

Whisper sometimes messes up technical symbols. The confirmation step helps but does not fix it automatically. The user must re-speak more clearly.

The wake word threshold of 0.9 means you have to say "Hey Jarvis" fairly clearly. In a noisy room it might miss sometimes. But I preferred that over constant false triggers.

The system is not 100% hands-free because confirmation still needs a spacebar press if you don't want to wait 15 seconds. I accepted this as a safety trade-off.

It only handles single-turn commands. There is no memory across wake words. That could be added later with Aider's chat mode.

Audio device handling is basic. On Windows it works without changes, but Linux or macOS might need manual device index configuration. 




9. Cost Analysis

For 100 interactions, each with about 20 seconds of speech and 500 tokens:

Local Whisper: $0
OpenWakeWord: $0
Groq LLM: $0 (free tier)

I initially tried OpenRouter but hit rate limits. Switched to Groq. It is fast, free, and good enough for this use case. No cost for the entire pipeline.

10. What I Learned

Local STT is good enough for developer tools. Whisper's accuracy combined with a confirmation step works in practice.

Tuning the wake word threshold is critical. A false positive rate of one per hour is fine; one per minute is not. 0.9 worked well.

Auto-accept with a timeout is a good balance. Most users will not wait the full 15 seconds; they either speak clearly or correct quickly.

Filtering subprocess output makes the terminal much cleaner for voice use.

Using Git as an automatic audit log gives a safety net for every voice command.

11. Possible Future Improvements

Add voice confirmation using a second wake word model for "accept" and "redo". That would eliminate the last keyboard press.

Maintain conversation history with Aider's chat mode so the user can ask follow-up questions without repeating the wake word.

Add voice commands for undo, show status, and explain last change.

Automatically detect the default microphone instead of relying on device indices.

13. Conclusion

This project shows a near hands-free voice interface for a terminal coding agent. It reduces keyboard use to at most one keypress per interaction and often zero when auto-accept triggers. Local Whisper and OpenWakeWord keep it private and cost-free. The architecture is modular, so swapping STT or LLM backends is straightforward.

Setup time before demo: about 6-8 minutes to install dependencies, set GROQ_API_KEY, and run app.py.