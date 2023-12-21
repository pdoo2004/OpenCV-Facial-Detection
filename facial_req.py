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
import face_recognition 
import imutils 
import pickle 
import time 
import cv2 

# Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
# Determine faces from encodings.pickle file model created from train_model.py 
# (Refer to Notes Page)
encodingsP = "encodings.pickle"

# load the known faces and embeddings 
print("[INFO] loading encodings and face detector")
data = pickle.loads(open(encodingsP, "rb").read())

# Initialize videostream
vs = VideoStream(src=0,framerate=20).start()
time.sleep(2.0)

# start the FPS counter, currently running at average 1.33 fps
fps = FPS().start()


# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream 
	frame = vs.read()
	frame = imutils.resize(frame, width=400) #Smaller width = faster frame rate
	# Detect the face boxes
	boxes = face_recognition.face_locations(frame)
	# compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(frame, boxes)
	names = []

	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown" #if face is not recognized, then print Unknown

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

			# determine the recognized face with the largest number of votes
			name = max(counts, key=counts.get)

			#If someone in your dataset is identified, print their name on the screen
			if currentname != name:
				currentname = name
				print(currentname)

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

	# quit when 'q' key is pressed
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
