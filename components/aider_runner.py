import subprocess
import time

class AiderRunner:

    def git_auto_commit(self, message="auto commit"):
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)

    def run(self, prompt, filename=None):

        print("\nLaunching Aider...\n")

        cmd = [
            "aider",
            "--model", "groq/llama-3.3-70b-versatile",
            "--message", prompt,
            "--yes"
        ]

        if filename:
            cmd.append(filename)

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        start_time = time.time()
        output = ""

        while True:

            if time.time() - start_time > 120:
                process.terminate()
                print("\nAider timed out.")
                return

            line = process.stdout.readline()

            if not line:
                break

            line = line.strip()

            if not line:
                continue

            noisy_words = [
                "tokens",
                "cost:",
                "httpx",
                "litellm",
            ]

            if any(word in line.lower() for word in noisy_words):
                continue

            print(line)
            output += line + "\n"

        process.wait()

        # AUTO GIT COMMIT
        try:
            self.git_auto_commit(prompt[:60])
        except Exception as e:
            print(f"Git commit failed: {e}")

        return output