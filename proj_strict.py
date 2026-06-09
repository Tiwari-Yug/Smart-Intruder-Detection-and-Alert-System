import glob
import face_recognition
import cv2
import numpy as np
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ===============================
# Email Configuration
# ===============================
def send_email_alert(image_path, intruder_count):
    # ...existing code...
    SMTP_SERVER="smtp.gmail.com"
    SMTP_PORT=465
    sender_email = "damnb451@gmail.com"
    sender_password = "gtpt dsrx seyq ypfu"
    recipient_email = "1rn22ad055.yugtiwari@gmail.com"
    try:
        # ...existing code...
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"INTRUDER ALERT - Detection #{intruder_count}"
        # ...existing code...
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body = f"""
        SECURITY ALERT!
        An unknown person has been detected by your security system.
        Detection Time: {current_time}
        Detection Count: #{intruder_count}
        Image Location: {image_path}
        Please check the attached image and take appropriate action.
        This is an automated message from your security system.
        """
        msg.attach(MIMEText(body, 'plain'))
        with open(image_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= intruder_{intruder_count}.jpg')
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print(f" Email alert sent successfully for intruder #{intruder_count}")
    except Exception as e:
        print(f" Failed to send email: {str(e)}")

# ===============================
# Dataset Understanding and Encoding
# ===============================
paths = glob.glob('D:/project/data/*')
images = []
image_encodings = []
image_names = []
count_img = 0
print("Loading and encoding known faces...")
for i in paths:
    images.append(face_recognition.load_image_file(i))
    encodings = face_recognition.face_encodings(images[count_img])
    if encodings:
        image_encodings.append(encodings[0])
        image_names.append(i.split('/')[-1].split('.')[0])
    else:
        print(f"No face found in {i}")
    count_img += 1
print(f"Loaded {len(image_encodings)} faces")
os.makedirs('D:/project/intruders', exist_ok=True)
count = 0
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
process_this_frame = True
last_email_time = 0
email_cooldown = 30
# === Tolerance for matching (lower is stricter) ===
MATCH_TOLERANCE = 0.45  # Default is 0.6, lower value reduces false matches
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            name = "Unknown"
            if image_encodings:
                # Use compare_faces with stricter tolerance
                matches = face_recognition.compare_faces(image_encodings, face_encoding, tolerance=MATCH_TOLERANCE)
                face_distances = face_recognition.face_distance(image_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                # Accept match only if below stricter threshold
                if matches[best_match_index] and face_distances[best_match_index] < MATCH_TOLERANCE:
                    name = image_names[best_match_index]
            face_names.append(name)
    process_this_frame = not process_this_frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        if name == "Unknown":
            rectangle_color = (0, 0, 255)
            intruder_filename = f'D:/project/intruders/intru-{count}.jpg'
            cv2.imwrite(intruder_filename, frame)
            print(f"Intruder detected! Image saved as {intruder_filename}")
            current_time = datetime.now().timestamp()
            if current_time - last_email_time > email_cooldown:
                send_email_alert(intruder_filename, count)
                last_email_time = current_time
            count += 1
        else:
            rectangle_color = (0, 255, 0)
        cv2.rectangle(frame, (left, top), (right, bottom), rectangle_color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), rectangle_color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('f'):
        print("Exiting program...")
        break
cap.release()
cv2.destroyAllWindows()