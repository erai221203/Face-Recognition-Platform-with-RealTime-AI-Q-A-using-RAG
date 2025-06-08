from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import pickle
import numpy as np
import cv2
import io
import os

app = FastAPI()

DB_PATH = 'face_db.pkl'

if os.path.exists(DB_PATH):
    with open(DB_PATH, 'rb') as f:
        face_db = pickle.load(f)
else:
    face_db = {'encodings': [], 'names': []}

def save_db():
    with open(DB_PATH, 'wb') as f:
        pickle.dump(face_db, f)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
async def register(file: UploadFile, name: str = Form(...)):
    img_bytes = await file.read()
    img_np = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    face_locations = face_recognition.face_locations(img)
    if not face_locations:
        return {"status": "fail", "message": "No face detected"}

    encoding = face_recognition.face_encodings(img, face_locations)[0]
    face_db['encodings'].append(encoding)
    face_db['names'].append(name)
    save_db()

    return {"status": "success", "message": f"Registered {name}"}

@app.post("/recognize")
async def recognize(file: UploadFile):
    img_bytes = await file.read()
    img_np = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    face_locations = face_recognition.face_locations(img)
    if not face_locations:
        return {"status": "fail", "message": "No face detected"}

    encoding = face_recognition.face_encodings(img, face_locations)[0]
    matches = face_recognition.compare_faces(face_db['encodings'], encoding)
    name = "Unknown"
    if True in matches:
        idx = matches.index(True)
        name = face_db['names'][idx]

    return {"status": "success", "name": name}
