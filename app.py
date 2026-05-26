import keyboard
import sounddevice as sd
import time
import os

from openwakeword.model import Model
from openwakeword.utils import download_models

from components import VoiceRecorder
from components import Transcriber
from components import AiderRunner

recorder = VoiceRecorder()
transcriber = Transcriber()
aider_runner = AiderRunner()


# ---------------- AUTO WAKEWORD MODEL CHECK ----------------

print("Checking wake word models...")

try:
    model_path = "venv/lib/site-packages/openwakeword/resources/models/hey_jarvis_v0.1.onnx"

    if not os.path.exists(model_path):
        print("Wake word model missing. Downloading models...")
        download_models()

except Exception as e:
    print(f"Model check skipped: {e}")

print("Loading wake word model...")


# ---------------- CONFIRMATION SYSTEM ----------------

def confirm_execution(prompt):

    print("\nYou said:")
    print(prompt)

    print("\nOptions:")
    print("SPACE = accept")
    print("R = re-record")

    start_time = time.time()
    timeout = 15

    while True:

        elapsed = time.time() - start_time
        remaining = int(timeout - elapsed)

        if remaining >= 0:
            print(f"\rAuto-accept in: {remaining} sec", end="")

        if keyboard.is_pressed("space"):
            print("\nAccepted")
            return "accept"

        if keyboard.is_pressed("r"):
            print("\nRe-recording...")
            return "redo"

        if elapsed > timeout:
            print("\nAuto-accepted")
            return "accept"

        time.sleep(0.2)


def run_pipeline():

    while True:

        try:

            # ---------------- RECORD ----------------
            audio_file = recorder.record_voice()

            if audio_file is None:
                print("\nRecording cancelled.")
                break

            # ---------------- TRANSCRIBE ----------------
            prompt = transcriber.transcribe_audio(audio_file)

            if not prompt.strip():
                print("\nNo speech detected.")
                break

            # ---------------- CONFIRM ----------------
            decision = confirm_execution(prompt)

            if decision == "redo":
                continue

            # ---------------- RUN AIDER ----------------
            aider_runner.run(prompt)

            break

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            break

        except Exception as e:
            print(f"\nPipeline Error: {e}")
            time.sleep(1)


# ---------------- WAKE WORD INIT ----------------

print("Say 'Hey Jarvis' to start.")
print("Program exits after 30 seconds of inactivity.")

oww_model = Model(
    wakeword_models=["hey_jarvis"],
    inference_framework="onnx"
)

idle_timeout = 30
chunk_size = 1280

last_trigger_time = 0
cooldown = 3


# ---------------- MAIN LOOP ----------------

while True:

    start_time = time.time()

    print("\nListening for wake word...")

    try:

        with sd.InputStream(
            samplerate=16000,
            channels=1,
            dtype='int16',
        ) as stream:

            while True:

                # ---------------- AUTO EXIT ----------------
                if time.time() - start_time > idle_timeout:
                    print("\nNo activity for 30 seconds. Exiting...")
                    exit()

                # ---------------- AUDIO READ ----------------
                audio_chunk, overflowed = stream.read(chunk_size)

                if overflowed:
                    print("\nAudio overflow detected")

                audio_chunk = audio_chunk.flatten()

                # ---------------- WAKEWORD PREDICTION ----------------
                prediction = oww_model.predict(audio_chunk)
                score = prediction.get("hey_jarvis", 0.0)

                print(f"\rWake score: {score:.3f}", end="")

                # ---------------- WAKE DETECTED ----------------
                if (
                    score > 0.9 and
                    time.time() - last_trigger_time > cooldown
                ):

                    last_trigger_time = time.time()

                    print("\nWake word detected.")

                    break

                time.sleep(0.01)

        run_pipeline()

    except KeyboardInterrupt:
        print("\nExiting...")
        break

    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(1)