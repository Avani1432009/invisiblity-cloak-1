import cv2
import numpy as np
import time

# to save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output_file = cv2.VideoWriter("Output.avi", fourcc, 20.0, (640, 480))

# Starting the webcam
cap = cv2.VideoCapture(0)

# allowing the webcam to start by making the code to sleep for two seconds
time.sleep(2)
bg = 0

# capturing the background for 60 frames
for i in range(60):
    ret, bg = cap.read()

# fliping the background
bg = np.flip(bg, axis = 1)

# reading the capture frame until the camera is open
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break

# fliping the image for consistency
img = np.flip(img, axis = 1)

# converting the color to BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# generating the mask to detect red color
# these value can also be change as per the color
lower_red = np.array([0, 120, 50])
upper_red = np.array([10, 255, 255])
mask_1 = cv2.inRange(hsv, lower_red, upper_red)

lower_red = np.array([170, 120, 70])
upper_red = np.array([180, 255, 255])
mask_2 = cv2.inRange(hsv, lower_red, upper_red)

mask_1 = mask_1 + mask_2

# open and expand the image where there is mask 1
mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones(3,3), np.uint8)
mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones(3,3), np.uint8)

# selecting only the part that does not have mask 1 and saving in mask 2
mask_2 = cv2.bitwise_not(mask_1)

# keeping only part of the image without the red color or any color you may choose
res_1 = cv2.bitwise_and(img, img, mask = mask_2)

# keeping only part of the image with the red color or any color you may choose
res_2 = cv2.bitwise_and(img, img, mask = mask_1)

# generating the final output by merging the res_1 and res_2
final_output = cv2.addWeighted(res_1,1, res_2,0)
output_file.write(final_output)

# displaying the output to the user
cv2.imshow("magic", final_output)
cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()