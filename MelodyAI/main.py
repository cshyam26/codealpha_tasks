import numpy as np
import wave
import os
import torch
import torch.nn as nn
import pretty_midi

MODEL_PATH = "melody_model.pt"
OUTPUT_DIR = "outputs"
SEQ_LENGTH = 32


class MelodyLSTM(nn.Module):
    def __init__(self, vocab_size=128, embedding_dim=64, hidden_dim=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(
            embedding_dim, hidden_dim, batch_first=True
        )
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        x = self.embedding(x)
        x, hidden = self.lstm(x, hidden)
        return self.fc(x), hidden



import random

def generate_melody(model, seed, length=100, temperature=1.0):
    model.eval()
    notes = list(seed)
    hidden = None

    with torch.no_grad():
        # Process the starting notes once
        inputs = torch.tensor([notes], dtype=torch.long)
        embedded = model.embedding(inputs)
        _, hidden = model.lstm(embedded)

        for _ in range(length):
            # Predict the next note from the latest note
            last_note = torch.tensor([[notes[-1]]], dtype=torch.long)
            embedded = model.embedding(last_note)
            output, hidden = model.lstm(embedded, hidden)
            logits = model.fc(output[:, -1, :])

            # Sample with randomness
            probabilities = torch.softmax(
                logits / temperature, dim=-1
            )
            next_note = torch.multinomial(probabilities, 1).item()
            notes.append(next_note)

    return notes[len(seed):]


def save_midi(notes, filename):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    start = 0.0
    duration = 0.25

    for pitch in notes:
        instrument.notes.append(
            pretty_midi.Note(
                velocity=90,
                pitch=int(pitch),
                start=start,
                end=start + duration
            )
        )
        start += duration

    midi.instruments.append(instrument)
    midi.write(filename)


def save_wav(notes, filename):
    sample_rate = 44100
    note_duration = 0.30
    audio_parts = []

    for pitch in notes:
        frequency = 440.0 * (2 ** ((int(pitch) - 69) / 12))
        count = int(sample_rate * note_duration)
        t = np.arange(count) / sample_rate

        tone = (
            np.sin(2 * np.pi * frequency * t)
            + 0.3 * np.sin(4 * np.pi * frequency * t)
        )

        fade_length = int(sample_rate * 0.02)
        envelope = np.ones(count)
        envelope[:fade_length] = np.linspace(0, 1, fade_length)
        envelope[-fade_length:] = np.linspace(1, 0, fade_length)

        audio_parts.append(tone * envelope * 0.35)
        audio_parts.append(np.zeros(int(sample_rate * 0.03)))

    audio = np.concatenate(audio_parts)
    audio = np.clip(audio, -1, 1)
    audio = (audio * 32767).astype(np.int16)

    with wave.open(filename, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(audio.tobytes())

    print(f"WAV audio saved to: {filename}")


def main():
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Run: python train.py")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    model = MelodyLSTM()
    model.load_state_dict(
        torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    )

    # Starting notes for the melody
    seed = [60, 64, 67, 72] * 8

    generated_notes = generate_melody(model, seed, length=100)
    output_path = os.path.join(OUTPUT_DIR, "generated_melody.mid")

    save_midi(generated_notes, output_path)
    wav_path = os.path.join(OUTPUT_DIR, "generated_melody.wav")
    save_wav(generated_notes, wav_path)
    
    print("Melody generated successfully!")
    print(f"MIDI saved to: {output_path}")
    print("Open the MIDI file in a MIDI player or music editor.")


if __name__ == "__main__":
    main()
