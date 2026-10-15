
# VisionTrack AI — Object Detection and Tracking

A real-time computer vision application that detects
and tracks objects using a webcam.

Developed as part of the CodeAlpha AI Internship.

## Features

- Real-time object detection
- Object tracking with ByteTrack
- Bounding boxes and class labels
- Tracking IDs when available
- Live object count and FPS display
- Webcam video recording
- Keyboard controls for recording and exit

## Technologies Used

- Python
- OpenCV
- Ultralytics YOLO11
- ByteTrack

## Requirements

- Python 3.10 or later
- Webcam
- Internet connection for the initial model download

## Installation

Clone the repository:

    git clone YOUR_REPOSITORY_URL

Open the project directory:

    cd VisionTrackAI

Create a virtual environment:

    python -m venv .venv

Activate it on Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

Install dependencies:

    pip install ultralytics opencv-python

## Run the Application

    python main.py

## Controls

- Q: Quit the application
- R: Start or stop video recording

Recorded videos are saved in the runs directory.

## Model

The project uses the pretrained YOLO11 nano model.
The model weights are downloaded automatically
when required.

## Limitations

Detection accuracy and speed depend on lighting,
camera quality, hardware, and object visibility.
Tracking IDs may change when objects disappear
and reappear.

## Author

C Sai Shravan

## Project Purpose

Educational computer vision project developed
for the CodeAlpha AI Internship.
