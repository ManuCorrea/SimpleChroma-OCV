import cv2
import numpy as np

video = cv2.VideoCapture('video/city2.mp4')

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

def nothing(x):
    pass

# Create a window
cv2.namedWindow('image')

# Create trackbars for color change
# Hue is from 0-179 for Opencv
cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 0, 255, nothing)
# trackbar for erosion params
cv2.createTrackbar('kernel erosion', 'image', 0, 10, nothing)
cv2.createTrackbar('iterations erosion', 'image', 0, 10, nothing)
# trackbar for dilation params
cv2.createTrackbar('kernel dilation', 'image', 0, 10, nothing)
cv2.createTrackbar('iterations dilation', 'image', 0, 10, nothing)

cv2.setTrackbarPos('HMin', 'image', 0)
cv2.setTrackbarPos('SMin', 'image', 0)
cv2.setTrackbarPos('VMin', 'image', 0)
# Set default value for Max HSV trackbars
cv2.setTrackbarPos('HMax', 'image', 255)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

# Initialize HSV min/max values
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

while(1):
    ret, frame = video.read()
    if ret == True:
        ret, image = cap.read()
        # Get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin', 'image')
        sMin = cv2.getTrackbarPos('SMin', 'image')
        vMin = cv2.getTrackbarPos('VMin', 'image')
        hMax = cv2.getTrackbarPos('HMax', 'image')
        sMax = cv2.getTrackbarPos('SMax', 'image')
        vMax = cv2.getTrackbarPos('VMax', 'image')

        # Set minimum and maximum HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])
        # _, image = cap.read()
        # Convert to HSV format and color threshold
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)

        original = cv2.bitwise_and(image, image, mask=mask)    

        # resize video to same as video feed
        width, height, _ = image.shape
        frame = cv2.resize(frame, (height, width))

        # Print if there is a change in HSV value
        if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax

        kernel_size_erosion = cv2.getTrackbarPos('kernel erosion', 'image')
        kernel_erosion = np.ones((kernel_size_erosion,kernel_size_erosion),np.uint8)
        
        iterations_erosion = cv2.getTrackbarPos('iterations erosion', 'image')
        
        if kernel_size_erosion > 0 and iterations_erosion > 0:
            mask = cv2.erode(mask, kernel_erosion, iterations = iterations_erosion)
            result_ero = cv2.bitwise_and(image, image, mask=mask)
            cv2.imshow('erosion', result_ero)
        else:
            cv2.destroyWindow("erosion")

        kernel_size_dilation = cv2.getTrackbarPos('kernel dilation', 'image')
        kernel_dilation = np.ones((kernel_size_dilation, kernel_size_dilation), np.uint8)
        
        iterations_dilation = cv2.getTrackbarPos('iterations dilation', 'image')

        if kernel_size_dilation > 0 and iterations_dilation > 0:
            mask = cv2.dilate(mask,kernel_dilation,iterations = iterations_dilation)
            result_di = cv2.bitwise_and(image, image, mask=mask)
            cv2.imshow('dilatacion', result_di)

        result = cv2.bitwise_and(image, image, mask=mask)

        removeFromVideo = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))

        cv2.imshow('mask unprocess', original)
        cv2.imshow('image', result)
        cv2.imshow("final", result + removeFromVideo)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        # return to the beginning of the video
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)

cv2.destroyAllWindows()
