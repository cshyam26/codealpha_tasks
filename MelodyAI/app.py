
import os
import threading
from flask import Flask, render_template, request, send_from_directory
from musicgen_generate import generate_music

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
AUDIO_FILE = "musicgen_output.wav"
AUDIO_PATH = os.path.join(OUTPUT_DIR, AUDIO_FILE)

app = Flask(__name__)

# Prevent two requests from generating into the same file simultaneously.
generation_lock = threading.Lock()


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    generated = False
    prompt = ""

    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()

        if not prompt:
            error = "Please describe the music you want."
        elif len(prompt) > 1000:
            error = "Please keep your prompt under 1000 characters."
        elif not generation_lock.acquire(blocking=False):
            error = "Music is already being generated. Please try again shortly."
        else:
            try:
                os.makedirs(OUTPUT_DIR, exist_ok=True)

                if os.path.exists(AUDIO_PATH):
                    os.remove(AUDIO_PATH)

                generate_music(prompt, AUDIO_PATH)

                if os.path.isfile(AUDIO_PATH):
                    generated = True
                else:
                    error = "MusicGen finished, but the audio file was not created."

            except Exception as exc:
                app.logger.exception("Music generation failed")
                error = f"Music generation failed: {exc}"

            finally:
                generation_lock.release()

    return render_template(
        "index.html",
        error=error,
        generated=generated,
        prompt=prompt,
    )


@app.route("/audio/<path:filename>")
def audio(filename):
    if filename != AUDIO_FILE or not os.path.isfile(AUDIO_PATH):
        return "Audio file not found.", 404

    response = send_from_directory(
        OUTPUT_DIR,
        AUDIO_FILE,
        mimetype="audio/wav",
    )
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/download/<path:filename>")
def download(filename):
    if filename != AUDIO_FILE or not os.path.isfile(AUDIO_PATH):
        return "Audio file not found.", 404

    return send_from_directory(
        OUTPUT_DIR,
        AUDIO_FILE,
        as_attachment=True,
        download_name="melodyai_music.wav",
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
