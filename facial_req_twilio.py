#! /usr/bin/python

# import the necessary packages (Descriptions in the order they are imported)
# A class to facilitate video streaming from a webcam or Raspberry Pi camera.
# A class to keep track of frames per second in video stream processing.
# A library for recognizing and manipulating faces using deep learning.
# A library providing convenience functions for image processing using OpenCV.
# A module for serializing and deserializing Python object structures.
# A module providing various time-related functions.
# Open Source Computer Vision Library for real-time computer vision.

from imutils.video import VideoStream
from imutils.video import FPS
from twilio.rest import Client
import face_recognition
import imutils
import pickle
import time
import cv2
import requests

#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"
cascade = "haarcascade_frontalface_default.xml"
last_notification_time = 0
NOTIFICATION_COOLDOWN = 30  # Cooldown time in seconds


#Twilio Notifications
def send_message(name):
    # Twilio account SID and Auth Token
    account_sid = 'Placeholder'
    auth_token = 'Placeholder'
    # I cannot put the SID and token on a public repo
    # Create a Twilio client
    client = Client(account_sid, auth_token)
    
    # Your Twilio number and the number to send the SMS to
    from_number = '+18333220552'
    to_number = '+15715775669'
    
    # Create and send the message
    message = client.messages.create(
	from_=from_number,
        body=f"{name} is at your door.",
        to=to_number,
    )
    
    # Log the message SID
    print(f"Message SID: {message.sid}")

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0,framerate=20).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream and resize it 
	#(smaller=better)
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	
	# convert the input frame from BGR to grayscale (for face
	# detection) and 
	#from BGR to RGB (for face recognition)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

	#Creates box around face
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	# compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"

		# check to see if we have found a match
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)
		
			#If someone in your dataset is identified, print their name on the screen
		if currentname != name or (time.time() - last_notification_time) > NOTIFICATION_COOLDOWN:
			currentname = name
			print(currentname)

			last_notification_time = time.time()
				
			send_message(name)
			print('Notification sent.')
			
		# update the list of names
		names.append(name)

	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# draw the predicted face name on the image 
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 225), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			.8, (0, 255, 255), 2)

	# display the image to our screen
	cv2.imshow("Facial Recognition is Running", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("Elasped time: {:.2f}".format(fps.elapsed()))
print("FPS: {:.2f}".format(fps.fps()))

# End
cv2.destroyAllWindows()
vs.stop()
