import numpy as np
import cv2
#import winsound
import dlib

# load cascades
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('C:\\Python27\\Lib\\site-packages\\dlib\\shape_predictor_68_face_landmarks.dat')

inputName = '001_nonSleepy'
txtFile = open(inputName+'.txt', 'a')

#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter(fileName+'_output.avi', fourcc, 30.0, (640, 360))

# play sound
#FREQ = 2500
#DURATION = 200  # in miliseconds

cap = cv2.VideoCapture('C:\\Users\\Itouch\\Desktop\\'+inputName+'.avi')
# ('C:\\Users\\Itouch\\Desktop\\burakDrive1.avi')

# set counters to measure number of frames
blinkCounter = 0
faceCounter = 0

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    if frame is not None:
        #frame = cv2.resize(frame, (640, 360))
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to grayscale
        # face detection
        faces = detector(grayFrame, 0)

        if len(faces) != 0: # face found
           faceCounter = 0
           # dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
           for k, d in enumerate(faces):
               # convert dlib rectangle object to opencv coordinates
               x = d.left()
               y = d.top()
               w = d.right() - x
               h = d.bottom() - y

               frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1) # put rectangle around face
               detected_landmarks = shape_predictor(frame, d).parts()  # detect landmarks

           landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])  # extract landmark coordinates

           leftH = ((landmarks[47][0, 1] - landmarks[43][0, 1]) + (landmarks[46][0, 1] - landmarks[44][0, 1]))   # left eye height
           leftW = (landmarks[45][0, 0] - landmarks[42][0, 0])   # left eye width 
           leftEAR = float(leftH) / (2 * leftW)   # left eye aspect ratio

           rightH = ((landmarks[41][0, 1] - landmarks[37][0, 1]) + (landmarks[40][0, 1] - landmarks[38][0, 1]))   # right eye height
           rightW = (landmarks[39][0, 0] - landmarks[36][0, 0])   # right eye width
           rightEAR = float(rightH) / (2 * rightW)   # right eye aspect ratio

           EAR = (leftEAR+rightEAR)/2.0   # eye aspect ratio

           if leftEAR < 0.25 or rightEAR < 0.25:  # either of the eyes is closed
               blinkCounter += 1
               cv2.putText(frame, 'EAR: {:.2}'.format(EAR), (grayFrame.shape[1]*8/10, grayFrame.shape[0]/10),
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, color=(0, 0, 255), thickness=1)

               if blinkCounter >= 12: # eyes are closed for more than 400 miliseconds
                   circleCenter = (grayFrame.shape[1]/10, grayFrame.shape[0]/10)
                   cv2.circle(frame, circleCenter, 20, color=(0, 0, 255), thickness = -1)
                   txtFile.write('1')
                   #winsound.Beep(FREQ, DURATION)
               else:
                   txtFile.write('0')
           else:   # eyes are open
               blinkCounter = 0
               txtFile.write('0')
               cv2.putText(frame, 'EAR: {:.2f}'.format(EAR), (grayFrame.shape[1]*8/10, grayFrame.shape[0]/10),
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, color=(255, 255, 0), thickness=1)

           for idx, point in enumerate(landmarks):
               if 35 < idx and idx < 48:
                   pos = (point[0, 0], point[0, 1])
                   # draw points on the landmark positions
                   cv2.circle(frame, pos, 1, color=(0, 255, 255))
                   # eyes points are from 36 to 47

        else: # face not found
           faceCounter += 1
           txtFile.write('0')
           if faceCounter >= 60:   # face not found more than 2 seconds
               txtFile.write('1')
               cv2.putText(frame, 'Watch the Road !', (grayFrame.shape[1]/15, grayFrame.shape[0]*9/10),
                   cv2.FONT_HERSHEY_COMPLEX, 0.5, color=(0, 0, 255), thickness=1)


        #out.write(frame)
        cv2.imshow('display', frame)


    else:
        print 'unable to read next frame'
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# for (x,y,w,h) in faces:
# frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

# cv2.namedWindow('display',cv2.WINDOW_NORMAL)
# cv2.resizeWindow('display', 1280,720)
