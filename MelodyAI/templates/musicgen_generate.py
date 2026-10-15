import os
import torch
import scipy.io.wavfile as wavfile
from transformers import AutoProcessor, MusicgenForConditionalGeneration

MODEL_NAME = "facebook/musicgen-small"
OUTPUT_DIR = "outputs"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading MusicGen on {device}...")
    print("The first run downloads the pretrained model.")

    processor = AutoProcessor.from_pretrained(MODEL_NAME)
    model = MusicgenForConditionalGeneration.from_pretrained(MODEL_NAME)
    model = model.to(device)
    model.eval()

    prompt = input(
        "Describe the music you want: "
    ).strip()

    if not prompt:
        prompt = "Peaceful piano melody with warm cinematic strings"

    inputs = processor(
        text=[prompt],
        padding=True,
        return_tensors="pt"
    ).to(device)

    print("Generating music. Please wait...")

    with torch.no_grad():
        audio = model.generate(
            **inputs,
            do_sample=True,
            guidance_scale=3,
            max_new_tokens=256
        )

    audio_array = audio[0, 0].cpu().numpy()
    sample_rate = model.config.audio_encoder.sampling_rate

    # Save audio as a standard WAV file.
    audio_array = audio_array.clip(-1, 1)
    audio_array = (audio_array * 32767).astype("int16")

    output_path = os.path.join(
        OUTPUT_DIR, "musicgen_output.wav"
    )
    wavfile.write(output_path, sample_rate, audio_array)

    print(f"Music generated successfully: {output_path}")


if __name__ == "__main__":
    main()
