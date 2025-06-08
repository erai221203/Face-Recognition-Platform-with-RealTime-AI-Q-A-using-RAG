import face_recognition
import pickle
import cv2
import sys
import os
import datetime

DB_PATH = '../server/face_db.pkl'
IMG_PATH = '../server/temp.jpg'
LOG_PATH = '../logs/events.log'

# Load or initialize DB
if os.path.exists(DB_PATH):
    with open(DB_PATH, 'rb') as f:
        face_db = pickle.load(f)
else:
    face_db = {'encodings': [], 'names': []}

def save_db():
    with open(DB_PATH, 'wb') as f:
        pickle.dump(face_db, f)

def log_registration(name):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, 'a') as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - Name: {name} registered\n")

def register(name):
    img = cv2.imread(IMG_PATH)
    locations = face_recognition.face_locations(img)
    if not locations:
        print("No face found")
        return
    enc = face_recognition.face_encodings(img, locations)[0]
    face_db['encodings'].append(enc)
    face_db['names'].append(name)
    save_db()
    log_registration(name)
    print(f"Registered face for {name}")

def recognize():
    img = cv2.imread(IMG_PATH)
    locations = face_recognition.face_locations(img)
    if not locations:
        print('{"status": "fail", "message": "No face found"}')
        return
    enc = face_recognition.face_encodings(img, locations)[0]
    matches = face_recognition.compare_faces(face_db['encodings'], enc)
    name = "Unknown"
    if True in matches:
        idx = matches.index(True)
        name = face_db['names'][idx]
    print(f'{{"status": "success", "name": "{name}"}}')

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "register":
        register(sys.argv[2])
    elif sys.argv[1] == "recognize":
        recognize()
