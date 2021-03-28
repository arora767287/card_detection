import cv2
import numpy as np
import imutils
from imutils import contours
import pytesseract
#Analyzes contours (which are later used as regions of interest) of the the template image of the NRIC
def template_image(template_img, img_fields):
    img = cv2.imread(img_fields)
    img = np.array(img)

    blank_img = cv2.imread(template_img)
    blank_img = np.array(blank_img)
    
    #image processing operations on the template image
    ret, thresh = cv2.threshold(img,127,200,cv2.THRESH_BINARY)

    gray_image = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

    retl, threshl = cv2.threshold(img,30,200,cv2.THRESH_BINARY_INV)

    gray = cv2.cvtColor(threshl, cv2.COLOR_BGR2GRAY)

    #Finds contours along the black rectangles on the template image
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Finds the external outline contour of the image
    contour, hierarch = cv2.findContours(grayimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #Store contours in an array
    c = np.array([contours[0],contours[1],contours[2],contours[3],contours[4],contours[21], contour[0]])
    return c
#Attaches contours to the regions of interest and fields that they correspond to while turning the contours into rectangles
def information(contours):
    #List of all fields that are important on the front of the NRIC Card
    placement = ['nationality', 'date of birth', 'gender', 'name', 'picture', 'fin_number', 'entire']
    #
    contour_rectangles = {
        'name': 0,
        'date of birth': 0,
        'gender': 0,
        'nationality': 0,
        'fin_number': 0,
        'picture': 0,
        'entire':0
    }
    boundRect = [None]*len(contours)
    contours_poly = [None]*len(contours)
    
    #Finds the center of every contour and creates a bounding box around it
    #Stores the center and bounding box in the contours_rectangle dictionary of regions of interest
    for i in range(0, len(contours)):
        center = cv2.moments(contours[i])
        if(center["m00"]==0):
            center["m00"] = 1
        centerX = int(center["m10"]/center["m00"])
        centerY = int(center["m01"]/center["m00"])
        contours_poly[i] = cv2.approxPolyDP(contours[i], 3, True)
        boundRect[i] = cv2.boundingRect(contours_poly[i])
        contour_rectangles[placement[i]] = [boundRect[i], centerX, centerY]
    return contour_rectangles   
#Takes the image url to the picture of the NRIC and executes option 2 by cropping unnecessary parts of the image away
def input_image(image_url):
    ratio = 10
    initial = cv2.imread(image_url)
    width = int(initial.shape[1] * (100/ratio) / 100)
    height = int(initial.shape[0] * (100/ratio) / 100)

    # desired size of resized picture of NRIC
    dsize = (width, height)
    image = cv2.resize(initial,dsize)

    #Image processing operations to analyze the largest contour of the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 60, 70)
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(contours, key = cv2.contourArea, reverse=True)[:5]
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then assume that NRIC card has been found
        if len(approx) == 4:
            screenCnt = approx
            break
    # store the bounded rectangle version of the contour
    rectangle = cv2.boundingRect(screenCnt)

    #Rescale the contour surrounding the NRIC card and the image to their original size
    x_value, y_value, newwidth, newheight = rectangle
    centerX = x_value+(newwidth/2)
    centerY = y_value+(newheight/2)

    initialwidth = initial.shape[1]
    initialheight = initial.shape[0]
    initialCenterX = initialwidth/2
    initialCenterY = initialheight/2

    resizedCenterX = width/2
    resizedCenterY = height/2

    lengthX = (resizedCenterX-centerX)
    lengthY = (resizedCenterY-centerY)
    lengthX = lengthX*ratio
    lengthY = lengthY*ratio

    rectangleInitialX = initialCenterX-lengthX
    rectangleInitialY = initialCenterY-lengthY

    initialRectangleHeight = newheight*ratio
    initialRectangleWidth = newwidth*ratio
    rectangleX = rectangleInitialX - initialRectangleWidth/2
    rectangleY = rectangleInitialY - initialRectangleHeight/2

    #Return the part of the image with the NRIC card (crop the image based on the position of the rectangle)
    return initial[int(rectangleY):int(rectangleY+initialRectangleHeight), int(rectangleX):int(rectangleX+initialRectangleWidth)]

# Callback function that executes if the user wants to crop the input image themselves to identify the NRIC card's location in the image   
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
    cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 9)
    #cv2.imshow("images.png", image)

#Scales the NRIC image to be analysed to the size of the template image to match the two NRIC cards and find regions of interest
def scaled(contour_rectangles, picture):    
    picture = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)

    array_information = contour_rectangles['entire']
    #Finds the width and height of the template image
    maximum_width = array_information[0][2]
    maximum_height = array_information[0][3]

    #Finds outline contour of image
    contours, hierarchy = cv2.findContours(picture, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #Approximates bounding box around the outline contour of the input image
    contours_poly_img = cv2.approxPolyDP(contours[0], 3, True)
    #Finds the width and height of the input image
    rect_img_width = cv2.boundingRect(contours_poly_img)[2]
    rect_img_height = cv2.boundingRect(contours_poly_img)[3]
    #Finds the center of the input image
    img_centerX = maximum_width/2.0
    img_centerY = maximum_height/2.0
    #Finds the scaling factor to resize the input image to the size of the template image
    scalingX = float(rect_img_width)/maximum_width
    scalingY = float(rect_img_height)/maximum_height
    #Resizes the input image
    picture_resize = cv2.resize(picture, (maximum_width, maximum_height), fx=scalingX, fy=scalingY)
    return picture_resize
#Goes through the dictionary and fills out each field using the output of OCR from the regions of interest corresponding to each field on the card
def find_information(image_information, picture):
    information = {
    'name': '',
    'date of birth': '',
    'gender': '',
    'nationality': '',
    'fin_number': '',
    'picture': '',
    'entire': ''
    }
    #Uses OCR on each region of interest through slicing the input image on each bounding rectangle and puts information in the dictionary
    for key, coordinate in image_information.items():
        y = image_information[key][0][1]
        h = image_information[key][0][3]
        x = image_information[key][0][0]
        w = image_information[key][0][2]
        ROI = picture[y:y+h,x:x+w]
        data = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6')
        information[key] = data
    return information
#Program 
lines = template_image("image_new.png", "image_new_copy.png")
rectangles = information(lines)
img_url = input("Insert image path (or just drag and drop the image into terminal): ")

option = input("Crop or not crop image")
#If the user wants to crop the image themselves
if option == '1':
    image = cv2.imread(img_url)
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
        # from the image and display it
        if len(ref_point) == 2:
            picture = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
    #cv2.imshow("crop_img", crop_img)
#If the user wants to make the computer crop the image
elif option == '2':
    picture = input_image(img_url)
scaledimg = scaled(rectangles, picture)
information = find_information(rectangles, scaledimg)
print("Name: " + information['name'])
print("Date Of Birth: " + information['date of birth'])
print("Nationality: " + information['nationality'])
print("FIN Number: " + information['fin_number'])
