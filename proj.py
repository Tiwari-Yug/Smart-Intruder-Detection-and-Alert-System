# Import required libraries
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
    """Send email notification when intruder is detected"""
    
    # Email configuration - UPDATE THESE WITH YOUR DETAILS
    SMTP_SERVER="smtp.gmail.com"
    SMTP_PORT=465
    sender_email = "damnb451@gmail.com"  # Your email address
    sender_password = "gtpt dsrx seyq ypfu"   # Your app password (not regular password)
    recipient_email = "1rn22ad055.yugtiwari@gmail.com" # Email to receive alerts
    
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"🚨 INTRUDER ALERT - Detection #{intruder_count}"
        
        # Email body
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
        
        # Attach the image
        with open(image_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= intruder_{intruder_count}.jpg'
        )
        msg.attach(part)
        
        # Gmail SMTP configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"✅ Email alert sent successfully for intruder #{intruder_count}")
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")

# ===============================
# Dataset Understanding and Encoding
# ===============================
paths = glob.glob('D:/project/data/*')  # Corrected path
images = []
image_encodings = []
image_names = []
count_img = 0

print("Loading and encoding known faces...")
for i in paths:
    images.append(face_recognition.load_image_file(i))
    
    # Handle case when no face is found in the image
    encodings = face_recognition.face_encodings(images[count_img])
    if encodings:
        image_encodings.append(encodings[0])
        image_names.append(i.split('/')[-1].split('.')[0])
    else:
        print(f"No face found in {i}")
    
    count_img += 1
print(f"Loaded {len(image_encodings)} faces")

# Create intruders directory if it doesn't exist
os.makedirs('D:/project/intruders', exist_ok=True)
count = 0
cap = cv2.VideoCapture(0)

# Set lower resolution for faster processing
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Process only every few frames for better performance
process_this_frame = True

# Email cooldown to prevent spam (send email only once every 30 seconds)
last_email_time = 0
email_cooldown = 30  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Only process every other frame to save time
    if process_this_frame:
        # Resize frame to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Convert BGR to RGB (face_recognition uses RGB)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            name = "Unknown"
            if image_encodings:
                matches = face_recognition.compare_faces(image_encodings, face_encoding)
                
                # Calculate face distance and find best match
                face_distances = face_recognition.face_distance(image_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = image_names[best_match_index]
                    
            face_names.append(name)
    
    process_this_frame = not process_this_frame
    
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
        # Set rectangle color based on known/unknown face
        if name == "Unknown":
            # Red color for unknown faces (BGR format in OpenCV)
            rectangle_color = (0, 0, 255)
            
            # Save image of unknown face
            intruder_filename = f'D:/project/intruders/intru-{count}.jpg'
            cv2.imwrite(intruder_filename, frame)
            print(f"Intruder detected! Image saved as {intruder_filename}")
            
            # Send email alert with cooldown
            current_time = datetime.now().timestamp()
            if current_time - last_email_time > email_cooldown:
                send_email_alert(intruder_filename, count)
                last_email_time = current_time
            
            count += 1
        else:
            # Green color for known faces (BGR format in OpenCV)
            rectangle_color = (0, 255, 0)
        
        # Draw a box around the face with the appropriate color
        cv2.rectangle(frame, (left, top), (right, bottom), rectangle_color, 2)
        
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), rectangle_color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    # Display the resulting image
    cv2.imshow('Video', frame)
    
    # Press 'q' or 'f' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('f'):
        print("Exiting program...")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
#first activate virtual environment & D:/project/.venv/Scripts/Activate.ps1