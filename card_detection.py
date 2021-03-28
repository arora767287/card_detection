import cv2
import numpy as np
import imutils
from imutils import contours
import PySimpleGUI
import sympy
import matplotlib
from document import Warper
import pytesseract

# Read the image and transform it to HSV color space

img = cv2.imread("image_new_copy.png")
blank_img = cv2.imread("image_new.png")
blank_img = np.array(blank_img)
img = np.array(img)

ret, thresh = cv2.threshold(img,127,200,cv2.THRESH_BINARY)

gray_image = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

retl, threshl = cv2.threshold(img,30,200,cv2.THRESH_BINARY_INV)

gray = cv2.cvtColor(threshl, cv2.COLOR_BGR2GRAY)

contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
contour, hierarch = cv2.findContours(grayimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(len(contour))
cv2.drawContours(blank_img, contour, -1, (0,0,255),1)
c = np.array([contours[0],contours[1],contours[2],contours[3],contours[4],contours[21], contour[0]])
cv2.drawContours(blank_img, c, -1, (0,0,255), 1)

placement = ['nationality', 'gender', 'date of birth', 'name', 'picture', 'fin_number', 'entire']
contour_rectangles = {
    'name': 0,
    'gender': 0,
    'date of birth': 0,
    'nationality': 0,
    'fin_number': 0,
    'picture': 0,
    'entire':0
}
boundRect = [None]*len(c)
contours_poly = [None]*len(c)

for i in range(0, len(c)):
    center = cv2.moments(c[i])
    if(center["m00"]==0):
        center["m00"] = 1
    centerX = int(center["m10"]/center["m00"])
    centerY = int(center["m01"]/center["m00"])
    cv2.drawContours(blank_img, c[i], -1, (0,255,0), 2)
    cv2.circle(blank_img, (centerX, centerY), 12, (255,255,255),-1)
    cv2.putText(blank_img, "center " + str(i), (centerX-20, centerY-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
    contours_poly[i] = cv2.approxPolyDP(c[i], 3, True)
    boundRect[i] = cv2.boundingRect(contours_poly[i])
    contour_rectangles[placement[i]] = [boundRect[i], centerX, centerY]

ref_point = []
cropping = False

def shape_selection(event, x, y, flags, param):
  # grab references to the global variables
  global ref_point, cropping

  # if the left mouse button was clicked, record the starting
  # (x, y) coordinates and indicate that cropping is being
  # performed
  if event == cv2.EVENT_LBUTTONDOWN:
    ref_point = [(x, y)]
    cropping = True

  # check to see if the left mouse button was released
  elif event == cv2.EVENT_LBUTTONUP:
    # record the ending (x, y) coordinates and indicate that
    # the cropping operation is finished
    ref_point.append((x, y))
    cropping = False

    # draw a rectangle around the region of interest
    cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 12)
    cv2.imshow("images.png", image)

# load the image, clone it, and setup the mouse callback function
image = cv2.imread("images.png")
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)

# keep looping until the 'q' key is pressed
while True:
  # display the image and wait for a keypress
  cv2.imshow("image", image)
  key = cv2.waitKey(1) & 0xFF

  # if the 'r' key is pressed, reset the cropping region
  if key == ord("r"):
    image = clone.copy()

  # if the 'c' key is pressed, break from the loop
  elif key == ord("c"):
    break

# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(ref_point) == 2:
  picture = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
  #cv2.imshow("crop_img", crop_img)

#picture = cv2.imread("images.png")
#picture = np.array(picture)
picture = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
array_information = contour_rectangles['entire']
maximum_width = array_information[0][2]
maximum_height = array_information[0][3]
contours, hierarchy = cv2.findContours(picture, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_poly_img = cv2.approxPolyDP(contours[0], 3, True)
rect_img_width = cv2.boundingRect(contours_poly_img)[2]
rect_img_height = cv2.boundingRect(contours_poly_img)[3]
img_centerX = maximum_width/2.0
img_centerY = maximum_height/2.0
scalingX = float(rect_img_width)/maximum_width
scalingY = float(rect_img_height)/maximum_height
picture_resize = cv2.resize(picture, (maximum_width, maximum_height), fx=scalingX, fy=scalingY)


#thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
def find_information(image_information, picture):
    information = {
    'name': '',
    'gender': '',
    'date of birth': '',
    'nationality': '',
    'fin_number': '',
    'picture': '',
    'entire': ''
    }
    for key, coordinate in image_information.items():
        y = image_information[key][0][1]
        h = image_information[key][0][3]
        x = image_information[key][0][0]
        w = image_information[key][0][2]
        ROI = picture[y:y+h,x:x+w]
        data = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6')
        information[key] = data
    return information



#print(find_information(contour_rectangles, picture_resize))
cv2.imshow("Picture", picture_resize)
cv2.imshow("Picture Picture", picture)
print(contour_rectangles)
cv2.imshow('Image', blank_img)
cv2.waitKey(10000000)
