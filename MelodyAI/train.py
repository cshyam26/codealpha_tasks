import os
import glob
import numpy as np
import pretty_midi
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

DATASET_DIR = "dataset"
MODEL_PATH = "melody_model.pt"
SEQ_LENGTH = 32
EPOCHS = 30


class MelodyDataset(Dataset):
    def __init__(self, midi_files):
        self.sequences = []

        for file in midi_files:
            try:
                midi = pretty_midi.PrettyMIDI(file)
                notes = []

                for instrument in midi.instruments:
                    if not instrument.is_drum:
                        notes.extend(
                            note.pitch for note in instrument.notes
                        )

                if len(notes) > SEQ_LENGTH:
                    for i in range(len(notes) - SEQ_LENGTH):
                        self.sequences.append(
                            notes[i:i + SEQ_LENGTH + 1]
                        )
            except Exception as error:
                print(f"Skipping {file}: {error}")

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, index):
        sequence = torch.tensor(
            self.sequences[index], dtype=torch.long
        )
        return sequence[:-1], sequence[1:]


class MelodyLSTM(nn.Module):
    def __init__(self, vocab_size=128, embedding_dim=64, hidden_dim=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(
            embedding_dim, hidden_dim, batch_first=True
        )
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.lstm(x)
        return self.fc(x)


def main():
    midi_files = glob.glob(os.path.join(DATASET_DIR, "*.mid"))
    midi_files += glob.glob(os.path.join(DATASET_DIR, "*.midi"))

    if not midi_files:
        print("No MIDI files found in the dataset folder.")
        print("Add some .mid or .midi files to dataset/ and try again.")
        return

    dataset = MelodyDataset(midi_files)

    if len(dataset) == 0:
        print("Not enough usable notes to train. Add longer MIDI files.")
        return

    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    model = MelodyLSTM()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    print(f"Training on {len(dataset)} note sequences...")

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0.0

        for inputs, targets in loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(
                outputs.reshape(-1, 128),
                targets.reshape(-1)
            )
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(
            f"Epoch {epoch + 1}/{EPOCHS} | "
            f"Loss: {total_loss / len(loader):.4f}"
        )

    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Training complete! Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
