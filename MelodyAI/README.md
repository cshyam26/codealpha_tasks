# 🎵 MelodyAI — AI Music Generator

MelodyAI is an AI-powered music generation web application that transforms text descriptions and emotions into instrumental music. Users can select a mood, customize a music prompt, generate audio, listen to the result, and download it as a WAV file.

## ✨ Features

- **Text-to-music generation:** Generate instrumental music from natural-language descriptions using Meta's MusicGen Small model.
- **Mood-based presets:** Explore Sad, Relaxing, Cinematic, and Hopeful music.
- **Multiple variations:** Choose styles such as heartbreak, rainy night, meditation, lo-fi study, epic adventure, sci-fi, motivation, and more.
- **Custom prompts:** Describe your own musical ideas and emotional atmosphere.
- **Audio playback:** Listen to generated music directly in the browser.
- **WAV download:** Save generated music locally.
- **Web interface:** Use a Flask-powered interface without running a separate command for every generation.

## 🛠️ Technologies Used

- Python
- Flask
- PyTorch
- Hugging Face Transformers
- Meta MusicGen Small
- HTML
- CSS
- JavaScript

## ⚙️ Installation and Setup


### 1. Clone the repository

```bash
git clone https://github.com/cshyam26/CodeAlpha_MelodyAI.git
cd CodeAlpha_MelodyAI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the required packages:

```bash
python -m pip install flask torch transformers scipy accelerate
```

A compatible PyTorch installation and sufficient system resources are required. The pretrained model may need to download on the first run.

### 4. Start the application

```bash
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

## 🎼 How to Use

1. Start the Flask application.
2. Open the website in your browser.
3. Select a music mood or one of its variations.
4. Edit the prompt if desired.
5. Click **Generate Music** and wait for generation to finish.
6. Play the resulting audio or download the WAV file.

## 📁 Project Structure

```text
MelodyAI/
├── app.py
├── musicgen_generate.py
├── templates/
│   └── index.html
├── outputs/
├── README.md
└── .gitignore
```

Additional training scripts or legacy model files may remain in the local project.

## ⚠️ Notes and Limitations

- The first generation may take longer while the pretrained model downloads and loads.
- Generation speed depends on available RAM, GPU, and other hardware resources.
- MusicGen outputs can vary between generations and may not perfectly match every prompt.
- This project currently generates WAV audio rather than MIDI compositions.
- Generated audio and model files can require substantial disk space.

## 📜 Model License

This project uses `facebook/musicgen-small`. Review the model's license and usage restrictions before distributing or using generated music, especially for commercial purposes.

Model information: https://huggingface.co/facebook/musicgen-small

## 🎯 Project Goal

MelodyAI demonstrates how generative AI, natural-language prompts, and a web interface can work together to create personalized instrumental music.

---

**Built as an AI music generation project.**