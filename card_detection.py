import cv2
import numpy as np
import imutils
from imutils import contours
import pytesseract
def template_image(template_img, img_fields):
    img = cv2.imread(img_fields)
    blank_img = cv2.imread(template_img)
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
    return c
def information(contours):
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
    boundRect = [None]*len(contours)
    contours_poly = [None]*len(contours)

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
def input_image(image_url):
	initial = cv2.imread(image_url)

	width = int(initial.shape[1] * 5 / 100)
	height = int(initial.shape[0] * 5 / 100)

	# dsize
	dsize = (width, height)
	image = cv2.resize(initial,dsize)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 60, 70)
	contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#cv2.drawContours(image, contours, -1, (0,255,0), 1)
	cnts = sorted(contours, key = cv2.contourArea, reverse=True)[:5]
	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if our approximated contour has four points, then we
		# can assume that we have found our screen
		if len(approx) == 4:
			screenCnt = approx
			break
	# show the contour (outline) of the piece of paper
	cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
	rectangle = cv2.boundingRect(screenCnt)
	print(rectangle)

	#Resized image width and height
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
	lengthX = lengthX*20
	lengthY = lengthY*20

	rectangleInitialX = initialCenterX-lengthX
	rectangleInitialY = initialCenterY-lengthY

	initialRectangleHeight = newheight*20
	initialRectangleWidth = newwidth*20
	rectangleX = rectangleInitialX - initialRectangleWidth/2
	rectangleY = rectangleInitialY - initialRectangleHeight/2

	print(int(rectangleY),int(rectangleY+initialRectangleHeight), int(rectangleX),int(rectangleX+initialRectangleWidth))
	return initial[int(rectangleY):int(rectangleY+initialRectangleHeight), int(rectangleX):int(rectangleX+initialRectangleWidth)]

#picture is the input picture and contours are from template
def scaled(contour_rectangles, picture):    
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
    return picture_resize

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

lines = template_image("image_new.png", "image_new_copy.png")
rectangles = information(lines)
picture = input_image("img.png")
scaledimg = scaled(rectangles, picture)
information = find_information(rectangles, scaledimg)
print(information)
