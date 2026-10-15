
import os
import sys
import torch
import scipy.io.wavfile as wavfile
from transformers import AutoProcessor, MusicgenForConditionalGeneration

MODEL_NAME = "facebook/musicgen-small"

# Keep the loaded model in memory for reuse.
processor = None
model = None
device = None


def load_model():
    global processor, model, device

    if model is not None:
        return

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading MusicGen on {device}...", flush=True)

    processor = AutoProcessor.from_pretrained(MODEL_NAME)
    model = MusicgenForConditionalGeneration.from_pretrained(MODEL_NAME)
    model = model.to(device)
    model.eval()

    print("MusicGen is ready!", flush=True)


def generate_music(prompt, output_path):
    load_model()

    inputs = processor(
        text=[prompt],
        padding=True,
        return_tensors="pt",
    ).to(device)

    print("Generating music...", flush=True)

    with torch.inference_mode():
        audio = model.generate(
            **inputs,
            do_sample=True,
            guidance_scale=3,
            max_new_tokens=1024,
        )

    audio_array = audio[0, 0].cpu().numpy()
    sample_rate = model.config.audio_encoder.sampling_rate
    audio_array = (
        audio_array.clip(-1, 1) * 32767
    ).astype("int16")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wavfile.write(output_path, sample_rate, audio_array)

    print(f"Success! Audio saved to {output_path}", flush=True)
    return output_path


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(
        base_dir, "outputs", "musicgen_output.wav"
    )

    prompt = " ".join(sys.argv[1:]).strip()

    if not prompt:
        prompt = input("Describe your music: ").strip()

    if not prompt:
        prompt = "Peaceful piano with emotional cinematic strings"

    generate_music(prompt, output_path)


if __name__ == "__main__":
    main()
