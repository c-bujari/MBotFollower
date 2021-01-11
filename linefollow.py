import RPi.GPIO as GPIO
import cv2
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22

Motor2A = 19
Motor2B = 21
Motor2E = 23

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 160)
video_capture.set(4, 120)

try:
    while(True):
        # Capture the frames
        ret, frame = video_capture.read()
        
        # Crop the image
        crop_img = frame[60:120, 0:160]
        
         # Convert to grayscale
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        
        # Gaussian blur
        blur = cv2.GaussianBlur(gray,(5,5),0)
        
        # Color thresholding
        ret,thresh = cv2.threshold(blur,40,255,cv2.THRESH_BINARY_INV)
        
        # Find the contours of the frame
        contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
        
        # Find the biggest contour (if detected)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            
            M = cv2.moments(c)
            
            if M['m00'] == 0:
                continue
            
            cx = int(M['m10']/M['m00'])
            
            cy = int(M['m01']/M['m00'])
            
            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
            
            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
            
            if cx >= 120:
                print ("Turn Right")
                GPIO.output(Motor1A,GPIO.LOW)
                GPIO.output(Motor1B,GPIO.HIGH)
                GPIO.output(Motor1E,GPIO.HIGH)
                
                GPIO.output(Motor2E,GPIO.LOW)
                
            if cx < 120 and cx > 50:
                print ("On Track!")
                GPIO.output(Motor1A,GPIO.LOW)
                GPIO.output(Motor1B,GPIO.HIGH)
                GPIO.output(Motor1E,GPIO.HIGH)
                
                GPIO.output(Motor2A,GPIO.LOW)
                GPIO.output(Motor2B,GPIO.HIGH)
                GPIO.output(Motor2E,GPIO.HIGH)
                
            if cx <= 50:
                print ("Turn Left!")
                GPIO.output(Motor1E,GPIO.LOW)
                
                GPIO.output(Motor2A,GPIO.LOW)
                GPIO.output(Motor2B,GPIO.HIGH)
                GPIO.output(Motor2E,GPIO.HIGH)
                
        else:
            print ("I don't see the line")
            
        #Display the resulting frame
            
        cv2.imshow('frame',crop_img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
except ZeroDivisionError:
    print ("shitting myself")

print ("Stopping all")
GPIO.output(Motor1E,GPIO.LOW)
GPIO.output(Motor2E,GPIO.LOW)

GPIO.cleanup()
