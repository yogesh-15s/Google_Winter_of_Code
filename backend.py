from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import cv2
import numpy as np
import os

# -------------------- App Setup --------------------
app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load YOLOv8 model (people = class 0)
model = YOLO("yolov8n.pt")

# -------------------- Helper Function --------------------
def analyze_frame(frame):
    results = model(frame, classes=[0], verbose=False)
    count = len(results[0].boxes.cls)

    if count < 10:
        density = "LOW"
    elif count < 30:
        density = "MEDIUM"
    else:
        density = "HIGH"

    return count, density

# -------------------- Routes --------------------

# Home page
@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

# Analyze Image
@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        return {"error": "Invalid image"}

    count, density = analyze_frame(frame)

    return {
        "people_count": count,
        "density": density
    }

# Analyze Video
@app.post("/analyze/video")
async def analyze_video(file: UploadFile = File(...)):
    temp_path = "temp_video.mp4"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    cap = cv2.VideoCapture(temp_path)

    total_count = 0
    analyzed_frames = 0
    frame_id = 0
    FRAME_SKIP = 10  # analyze every 10th frame for speed

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % FRAME_SKIP == 0:
            count, _ = analyze_frame(frame)
            total_count += count
            analyzed_frames += 1

        frame_id += 1

    cap.release()
    os.remove(temp_path)

    if analyzed_frames == 0:
        return {"error": "Empty or invalid video"}

    avg_count = total_count // analyzed_frames

    if avg_count < 10:
        density = "LOW"
    elif avg_count < 30:
        density = "MEDIUM"
    else:
        density = "HIGH"

    return {
        "average_people_count": avg_count,
        "density": density
    }
