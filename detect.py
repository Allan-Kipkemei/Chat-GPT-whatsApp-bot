import cv2
import sqlite3
import time

def create_database():
    conn = sqlite3.connect("surveillance.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS detected_faces
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                       image BLOB)''')

    conn.commit()
    conn.close()

def store_detected_face(image):
    conn = sqlite3.connect("surveillance.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO detected_faces (image) VALUES (?)", (sqlite3.Binary(image),))

    conn.commit()
    conn.close()

def detect_and_save_face():
    # Change this path based on your OpenCV version (if the path is different)
    cascades_path = cv2.data.haarcascades if cv2.data else cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

    face_cascade = cv2.CascadeClassifier(cascades_path)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Save the detected face in the database
            detected_face = frame[y:y+h, x:x+w]
            store_detected_face(detected_face)

        cv2.imshow('Surveillance', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    create_database()
    detect_and_save_face()
