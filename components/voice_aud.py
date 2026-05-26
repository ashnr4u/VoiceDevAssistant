import keyboard
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import subprocess
import time
import numpy as np
import os

# ---------------- VOICE RECORDER ----------------

class VoiceRecorder:
    def __init__(self):
        self.fs = 16000
        self.channels = 1
        # self.device = 15 was using bluetooth

    def record_voice(self):

        silence_threshold = 0.003
        silence_duration = 2.0
        no_speech_timeout = 5.0
        max_record_time = 30

        print("\nListening... Speak now")

        audio_chunks = []

        start_time = time.time()
        silence_start = None
        speech_detected = False

        with sd.InputStream(
            samplerate=self.fs,
            channels=self.channels,
            # device=self.device,
            dtype='float32'
        ) as stream:

            while True:

                data, overflowed = stream.read(1024)

                audio_chunks.append(data)

                volume = np.abs(data).mean()

                print(f"\rVolume: {volume:.5f}", end="")

                # ---------------- SPEECH DETECTED ----------------
                if volume > silence_threshold:

                    speech_detected = True
                    silence_start = None

                # ---------------- SILENCE ----------------
                else:

                    # User never spoke
                    if not speech_detected:

                        if time.time() - start_time > no_speech_timeout:
                            print("\nNo speech detected.")
                            return None

                    # User spoke then became silent
                    else:

                        if silence_start is None:
                            silence_start = time.time()

                        elif time.time() - silence_start > silence_duration:
                            print("\nSilence detected. Stopping...")
                            break

                # ---------------- MAX TIME ----------------
                if time.time() - start_time > max_record_time:
                    print("\nMax recording time reached")
                    break

        recording = np.concatenate(audio_chunks, axis=0)

        write("output.wav", self.fs, recording)

        print("\nRecording saved")

        return "output.wav"

class Transcriber:
    def __init__(self):
        print("Loading Whisper model...")

        start = time.time()

        self.model = whisper.load_model("base")

        print(f"Whisper loaded in {round(time.time() - start, 2)} sec")

    def transcribe_audio(self, filename):

        print("\nTranscribing audio...")

        start = time.time()

        result = self.model.transcribe(filename)

        print(f"Transcription completed in {round(time.time() - start, 2)} sec")

        return result["text"]