import cv2 #Model of OpenCV
import os  # Import the os module

name = input("Enter the name of the subject: ")  # Get the name from user input


cam = cv2.VideoCapture(0)

cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("press space to take a photo", 600, 400)

# Check if directory exists, if not, create it
dir_name = "dataset/" + name
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
    
img_counter = 0
 
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k == ord("q"):
        # Q Pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
