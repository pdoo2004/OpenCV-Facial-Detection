# OpenCV-Facial-Detection

This project will focus on facial detection using OpenCV through a Rasbperry Pi 4.

How it works:

Image Capture: The system begins with capturing images through a USB webcam or a Pi Camera attached to the Raspberry Pi. This is done either through the headshots.py script for live capture or by uploading existing photos into individual folders named after each person in the dataset folder.

Model Training: The captured images are used to train the facial recognition model. The train_model.py script processes these images, detecting faces and extracting facial features. These features are then stored in an encodings.pickle file, creating a database of known faces.

Face Detection and Recognition: When the system is operational, the facial_req.py or facial_req_twilio.py script continuously captures video frames and uses the trained model to detect and recognize faces in real-time. Each detected face is compared against the known faces in the encodings.pickle file.

User Notification: Upon recognizing a face, the system checks if it's a known or unknown face. The system then uses Twilio's API to send a message stating "[name] is at your door".
