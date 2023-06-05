import cv2
from twilio.rest import Client
import tkinter as tk
from PIL import Image, ImageTk


import os

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)

# Twilio credentials
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
recipient_phone_number =os.environ.get('RECIPIENT_PHONE_NUMBER')

def send_sms_notification():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='Your security camera has detected a malicious person at your door. BE SAFE!!',
        from_=twilio_phone_number,
        to=recipient_phone_number
    )
    print('SMS notification sent successfully!')

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for x, y, w, h in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)

        image_name='saved.png'
        cv2.imwrite(image_name,faces)
    return faces

def update_frame():
    _, video_frame = video_capture.read()
    faces = detect_bounding_box(video_frame)
    cv2image = cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    label_video.configure(image=imgtk)
    label_video.image = imgtk

    if len(faces) > 0:
        send_sms_notification()

    label_video.after(10, update_frame)

# Create the main Tkinter window
root = tk.Tk()
root.title("Face Detection")
root.geometry("800x600")

# Create a label to display the video feed
label_video = tk.Label(root)
label_video.pack()

# Start updating the video feed
update_frame()

# Start the Tkinter event loop
root.mainloop()

# Release the video capture and destroy any remaining windows
video_capture.release()
cv2.destroyAllWindows()
