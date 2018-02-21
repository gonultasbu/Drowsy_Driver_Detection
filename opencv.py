import numpy as np
import cv2
import winsound
import dlib
#from matplotlib import pyplot as plt

#detector = dlib.get_frontal_face_detector()
face_cascade = cv2.CascadeClassifier('C:\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('C:\\opencv\\sources\\data\\haarcascades\\haarcascade_eye.xml')
shape_predictor = dlib.shape_predictor('C:\\Python27\\Lib\\site-packages\\dlib\\shape_predictor_68_face_landmarks.dat')

# play sound
FREQ = 2500
DURATION = 200 # in miliseconds
    
cap = cv2.VideoCapture(0)
#('C:\\Users\\Itouch\\Desktop\\okanDrive.avi')
if cap.isOpened():
  print('open')

#set counter to measure number of frames that eyes are closed   
counter = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    

    #face detection
    faces = face_cascade.detectMultiScale(grayFrame, 1.1, 10, minSize=(100,100))
    #dets = detector(grayFrame, 1)    
    if len(faces) != 0:
        for (x,y,w,h) in faces:
          dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        #for k, d in enumerate(dets):  
        detected_landmarks = shape_predictor(frame, dlib_rect).parts()   #detect landmarks          
        landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])  #extract coordinates
        
        leftH = ((landmarks[47][0,1]-landmarks[43][0,1]) + (landmarks[46][0,1]-landmarks[44][0,1]))
        leftW = (landmarks[45][0,0]-landmarks[42][0,0])
        leftEAR = float(leftH)/(2*leftW) 

        rightH = ((landmarks[41][0,1]-landmarks[37][0,1]) + (landmarks[40][0,1]-landmarks[38][0,1]))
        rightW = (landmarks[39][0,0]-landmarks[36][0,0])
        rightEAR = float(rightH)/(2*rightW)

        if leftEAR < 0.2 or rightEAR < 0.2:
          counter += 1
          if counter >=5:
            winsound.Beep(FREQ, DURATION)
        else:
          counter = 0
          
        for idx, point in enumerate(landmarks):
          if 35 < idx and idx < 48:            
            pos = (point[0, 0], point[0, 1])              
            # draw points on the landmark positions  
            cv2.circle(frame, pos, 3, color=(0, 255, 255))           
        #eyes points are from 36 to 47                   
            
    else:
        print('no face')
        #winsound.Beep(FREQ, DURATION)

    cv2.imshow('display',frame)
    #cv2.imshow('leftEye', leftEyeGray)  
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

'''
        for (x,y,w,h) in faces:
           frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
           roi_gray = grayFrame[y:y+h, x:x+w]           
           #Converting the OpenCV rectangle coordinates to Dlib rectangle  
           dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
''' 

#cv2.namedWindow('display_image',cv2.WINDOW_NORMAL)
#cv2.resizeWindow('display_image', 1280,720)

