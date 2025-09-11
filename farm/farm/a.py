# app/video_camera.py

import cv2

class VideoCamera:
    def __init__(self):
        self.thres = 0.45  # Confidence threshold for object detection
        self.cap = cv2.VideoCapture("http://10.144.127.65:8080/video")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 70)

        # Load class names
        classFile = "coco.names"
        with open(classFile, "rt") as f:
            self.classNames = f.read().rstrip("\n").split("\n")

        # Load DNN model
        configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        weightsPath = "frozen_inference_graph.pb"
        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def get_frame_and_objects(self):
        success, img = self.cap.read()
        detected_objects = []

        if not success or img is None:
            return None, []

        # Perform object detection
        try:
            classIds, confs, bbox = self.net.detect(img, confThreshold=self.thres)
        except cv2.error as e:
            print("OpenCV error during detection:", e)
            return None, []

        if classIds is not None and len(classIds) > 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                name = self.classNames[classId - 1].upper()

                # Only detect PERSON and COW, max 3 objects
                if name in ["PERSON", "COW"] and name not in detected_objects:
                    if len(detected_objects) < 3:
                        detected_objects.append(name)

                # Draw detection box and label
                cv2.rectangle(img, box, color=(0, 0, 255), thickness=2)
                cv2.putText(img, name, (box[0] + 10, box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
                cv2.putText(img, f"{round(confidence * 100, 2)}%", (box[0] + 200, box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        # Encode the frame to JPEG for streaming
        ret, jpeg = cv2.imencode('.jpg', img)
        if not ret:
            return None, []

        return jpeg.tobytes(), detected_objects







import cv2
import os
import numpy as np
import pickle
import csv
from datetime import datetime

class FaceRecognitionSystem:
    def __init__(self, data_path="opencv", face_size=(200, 200), model_path="face_model.yml", label_path="labels.pkl", attendance_path="attendance.csv"):
        self.data_path = data_path
        self.face_size = face_size
        self.model_path = model_path
        self.label_path = label_path
        self.attendance_path = attendance_path
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.label_map = {}
        
    def capture_faces(self, person_name, source=0, max_images=5):
        save_path = os.path.join(self.data_path, person_name)
        os.makedirs(save_path, exist_ok=True)
        cap = cv2.VideoCapture(source)
        count = 0
        print(f"📸 Starting face capture for '{person_name}' from source: {source}")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Couldn't read frame.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                count += 1
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, self.face_size)
                cv2.imwrite(f"{save_path}/{count}.jpg", face)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow("Capturing Faces - Press Q to Quit", frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or count >= max_images:
                break

        cap.release()
        cv2.destroyAllWindows()
        print(f"✅ Done capturing faces for {person_name}. Saved {count} images to {save_path}")

    def train_model(self):
        faces, labels = [], []
        label_id = 0
        self.label_map = {}

        for person in os.listdir(self.data_path):
            person_path = os.path.join(self.data_path, person)
            if not os.path.isdir(person_path):
                continue

            for img_name in os.listdir(person_path):
                img_path = os.path.join(person_path, img_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue

                face = cv2.resize(img, self.face_size)
                faces.append(face)
                labels.append(label_id)

            self.label_map[label_id] = person
            label_id += 1

        if not faces:
            print("[ERROR] No face data found.")
            return

        self.recognizer.train(faces, np.array(labels))
        self.recognizer.save(self.model_path)

        with open(self.label_path, "wb") as f:
            pickle.dump(self.label_map, f)

        print("[INFO] Training completed and model saved.")

    def recognize_and_mark_attendance(self, source=0, confidence_threshold=65):
        if not os.path.exists(self.model_path) or not os.path.exists(self.label_path):
            print("[ERROR] Model or label map not found. Train the model first.")
            return

        self.recognizer.read(self.model_path)
        with open(self.label_path, "rb") as f:
            self.label_map = pickle.load(f)

        cap = cv2.VideoCapture(source)
        print(f"🔍 Starting recognition from source: {source}")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Couldn't read frame.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                roi_resized = cv2.resize(roi, self.face_size)

                label, confidence = self.recognizer.predict(roi_resized)
                name = self.label_map.get(label, "Unknown")

                if confidence < confidence_threshold:
                    self.mark_attendance(name)
                else:
                    name = "Unknown"

                cv2.rectangle(frame, (x, y), (x+w, y+h), (229,255,0), 2)
                cv2.putText(frame, f"{name} {int(confidence)}", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)

            cv2.imshow("Face Attendance System", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def mark_attendance(self, name): # Already marked once in this run
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')
        with open(self.attendance_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, time_str, date_str])
            print(f"[ATTENDANCE] {name} marked at {time_str} on {date_str}")

        self.attendance_marked = True  # Set flag to prevent more entries



