# Foreigner (Green) NRIC Reader Code

This project takes in an NRIC card, scans the input, and returns the information contained on the card about the person who it belongs to. The information returned includes the person's name, their date of birth, their nationality, their FIN Number, and their gender. 

## Quick Links:

Dependencies
Starting The Code
How To Scan NRICs (Foreigners' Only)

## Dependencies

To use this program, install the following libraries using pip:
cv2
```bash
pip3 install opencv-python
```
numpy
```bash
pip3 install numpy
```
imutils
```bash
pip3 install imutils
```

## Starting The Code

In order to start the program, download the card_detection.py file or run it in an editor. 
Run the following command in your terminal (for Mac Users):
```bash
pip3 install card_detection_card.py
```

## How to scan NRICs

The program takes in landscape images of the NRIC card as input, so make sure the width of the input image is larger than its height. It also works best when the image
of the NRIC card is taken from a distance, and is centered in the frame of the picture (straightened). Having taken an image of the card which is straight is very helpful with making the information detection accurate.

Once the code starts, it will ask you for the file path to the image of your NRIC card. Then, it will give you two options. Press 1 to crop the original NRIC card out of the frame of your image (if it is noisy). Press 2 to proceed with the image selected as it is (if the background contrasts the card well).

For Option 1:

In order to crop the image, look for the tab labelled "Image" that opens up. The point on the image at which the mouse is first pressed is the first corner of the two-point rectangle used to crop the image. Drag your mouse to the second determining point of the rectangle and release. The region in green will be the part of the image that is saved. Try to capture as much of the NRIC card in the rectangle while avoiding the background. Press 'r' to reset the cropper and crop the original image again. Press 'c' to finalize the region outlines as the cropped version of your image.

For Option 2:

This is recommended for pictures that are on a clean background (solid color, very little noise), and requires no work on the part of the user.

The information about your card will be displayed in the terminal. Keep in mind that the program is very sensitive to changes in lighting, angle at which the picture is taken, and distance from the camera — a misinterpreted picture may be a mix of those factors. Simply retake the picture to analyze the card properly. 




