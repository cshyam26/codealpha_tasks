from ultralytics import YOLO
import cv2
import time
from pathlib import Path
from datetime import datetime

# ---------------- CONFIGURATION ----------------
MODEL_NAME = "yolo11n.pt"
CAMERA_INDEX = 0
CONFIDENCE = 0.35
OUTPUT_DIR = Path("runs")
# -----------------------------------------------


def main():
    print("Loading VisionTrack AI...")
    model = YOLO(MODEL_NAME)

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        print("Try changing CAMERA_INDEX to 1.")
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    recording = False
    video_writer = None
    previous_time = time.perf_counter()
    fps = 0.0

    print("\nVisionTrack AI is running!")
    print("Q = Quit | R = Start/stop video recording")

    while True:
        success, frame = camera.read()

        if not success:
            print("Unable to read webcam frame.")
            break

        # Detect and track objects in the current frame
        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=CONFIDENCE,
            verbose=False
        )

        result = results[0]
        display = result.plot()

        # Count detected objects and tracked IDs
        boxes = result.boxes
        object_count = len(boxes) if boxes is not None else 0
        tracked_count = 0

        if boxes is not None and boxes.id is not None:
            tracked_count = len(boxes.id)

        # Calculate FPS
        current_time = time.perf_counter()
        elapsed = current_time - previous_time

        if elapsed > 0:
            current_fps = 1.0 / elapsed
            fps = current_fps if fps == 0 else 0.85 * fps + 0.15 * current_fps

        previous_time = current_time

        # Dashboard overlay
        cv2.rectangle(display, (10, 10), (340, 120), (25, 25, 40), -1)

        cv2.putText(
            display, "VISIONTRACK AI", (22, 37),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 160, 255), 2
        )

        cv2.putText(
            display, f"Objects detected: {object_count}", (22, 65),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1
        )

        cv2.putText(
            display, f"Tracked IDs: {tracked_count}", (22, 89),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1
        )

        cv2.putText(
            display, f"FPS: {fps:.1f}", (22, 111),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (120, 255, 160), 1
        )

        # Recording status
        if recording:
            cv2.circle(display, (display.shape[1] - 35, 30), 8, (0, 0, 255), -1)
            cv2.putText(
                display, "REC", (display.shape[1] - 90, 36),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2
            )
            video_writer.write(display)

        cv2.imshow("VisionTrack AI | Object Detection & Tracking", display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        elif key == ord("r"):
            if not recording:
                OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

                filename = datetime.now().strftime(
                    "tracking_%Y%m%d_%H%M%S.mp4"
                )
                output_path = OUTPUT_DIR / filename

                height, width = display.shape[:2]
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")

                video_writer = cv2.VideoWriter(
                    str(output_path),
                    fourcc,
                    20.0,
                    (width, height)
                )

                if video_writer.isOpened():
                    recording = True
                    print(f"Recording to: {output_path}")
                else:
                    video_writer.release()
                    video_writer = None
                    print("Could not start recording.")

            else:
                recording = False
                video_writer.release()
                video_writer = None
                print("Recording saved.")

    # Release all resources
    if video_writer is not None:
        video_writer.release()

    camera.release()
    cv2.destroyAllWindows()
    print("VisionTrack AI closed successfully.")


if __name__ == "__main__":
    main()
