import cv2
import numpy as np
class Template():
    def __init__(self, document):
        if document == "Passport":
            self.img = cv2.imread("passport.png")
        elif document == "NRIC":
            self.img = cv2.imread("image_new_copy.png")
            print("NRIC")

        self.img = np.array(self.img)
        #image processing operations on the template image
        ret, thresh = cv2.threshold(self.img,127,200,cv2.THRESH_BINARY)

        gray_image = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

        retl, threshl = cv2.threshold(self.img,30,200,cv2.THRESH_BINARY_INV)

        gray = cv2.cvtColor(threshl, cv2.COLOR_BGR2GRAY)

        #Finds contours along the black rectangles on the template image
        self.contours, self.hierarchy = cv2.findContours(gray, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        grayimg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        #Finds the external outline contour of the image
        self.contour, self.hierarch = cv2.findContours(grayimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def NRIC(self):
        #Store contours in an array
        c = np.array([self.contours[0],self.contours[1],self.contours[2],self.contours[3],self.contours[4],self.contours[21], self.contour[0]])
        return c
    def passport(self):

        c = np.array([self.contours[6], self.contours[65], self.contours[138], self.contours[144], self.contours[146], self.contours[230], self.contours[231], self.contours[239], self.contours[269], self.contour[0]])
        return c
    def drivers_license(self):
'''
Class structure
Template Class
Drivers License Subclass 
Passport Subclass
NRIC subclass - Each region's NRIC type

