# -*- coding: utf-8 -*-
import numpy as np
import cv2
import winsound
import dlib

def process_video(input_file):
    # load detectors
    faceDetector = dlib.get_frontal_face_detector()
    shape_predictor = dlib.shape_predictor('C:\\Users\Mert\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\dlib\\shape_predictor_68_face_landmarks.dat')
    # get file names
    txtFile = open(input_file+'.txt', 'a')
    # adjust videoWriter settings
    #fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    #out = cv2.VideoWriter(inputName+'_output.avi', fourcc, 15.0, (640, 480))

    # play sound
    FREQ = 2500
    DURATION = 100  # in miliseconds
    def beep():
        winsound.Beep(FREQ, DURATION)

    cap = cv2.VideoCapture(input_file)   # read video file or stream
    # ('C:\\Users\\Itouch\\Desktop\\'+inputName+'.avi')

    N = 300   # max number of frames the list sample can have
    # set counters to measure number of frames
    blinkCounter = []
    faceCounter = 0

    # create list to find average threshold value for eye openness
    sample = []

    #TH = 0.25   # default threshold value for eye openness

    def detectFaces(frame):
        #frame = cv2.resize(frame, (640, 360))
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to grayscale
        faces = faceDetector(grayFrame, 0)

        return faces

    def removeOtherFaces(allFaces, frame):
        maxArea = 0
        for k, d in enumerate(allFaces):
                faceArea = (d.right() - d.left())*(d.bottom() - d.top())
                if faceArea > maxArea:
                    maxArea = faceArea
                    # convert dlib rectangle object to opencv coordinates
                    x = d.left()
                    y = d.top()
                    w = d.right() - x
                    h = d.bottom() - y
                    maxRect = d

        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1) # put rectangle around face
        return maxRect # return the biggest rectangle face area (diver's face)

    def detectFacialLandmarks(rectangle):
        detected_landmarks = shape_predictor(frame, rectangle).parts()  # detect landmarks
        landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])  # extract landmark coordinates

        return landmarks

    def leftEyeLandmarks(landmarks):
        leftH = ((landmarks[47][0, 1] - landmarks[43][0, 1]) + (landmarks[46][0, 1] - landmarks[44][0, 1])) # left eye height
        leftW = (landmarks[45][0, 0] - landmarks[42][0, 0]) # left eye width
        leftEAR = float(leftH) / (2 * leftW) # left eye EAR

        return leftEAR

    def rightEyeLandmarks(landmarks):
        rightH = ((landmarks[41][0, 1] - landmarks[37][0, 1]) + (landmarks[40][0, 1] - landmarks[38][0, 1])) # right eye height
        rightW = (landmarks[39][0, 0] - landmarks[36][0, 0]) # right eye width
        rightEAR = float(rightH) / (2 * rightW) # right eye EAR

        return rightEAR

    def setEyeAspectRatio(left, right):
        EAR = (left+right)/2.0   # eye aspect ratio
        return EAR

    def setThreshold(ear):
        if ear > 0.18:
            sample.append(ear)
        if len(sample) >= N:
            del sample[:len(sample)/2] # delete the first half of sample
        meanEAR = sum(sample)/float(len(sample))
        TH = meanEAR*0.8
        return TH

    def detectBlink(lEAR, rEAR, ear, threshold, countblink):
        if lEAR < threshold or rEAR < threshold:   # eyes are closed
            countblink.append(1)   # detect blink
            cv2.putText(frame, 'EAR: {:.2}'.format(ear), (frame.shape[1]*8/10, frame.shape[0]/10),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, color=(0, 0, 255), thickness=1)

            if len(countblink) >= 12:   # eyes are closed for more than 400 miliseconds
               circleCenter = (frame.shape[1]/10, frame.shape[0]/10)
               cv2.circle(frame, circleCenter, 20, color=(0, 0, 255), thickness = -1)
               txtFile.write('1')
               #beep()

            else:
               txtFile.write('0')
        else:   # eyes are open
            del countblink[:] # reset blink counter
            txtFile.write('0')
            cv2.putText(frame, 'EAR: {:.2f}'.format(ear), (frame.shape[1]*8/10, frame.shape[0]/10),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, color=(255, 255, 0), thickness=1)

    def drawEyeLandmarks(landmarks):
        for idx, point in enumerate(landmarks):
            if 35 < idx and idx < 48:
                pos = (point[0, 0], point[0, 1])
                # draw points on the landmark positions
                cv2.circle(frame, pos, 1, color=(0, 255, 255))
                # eyes points are from 36 to 47


    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()

        if frame is not None: # frame is not null
            faces = detectFaces(frame) # detect faces

            if len(faces) != 0: # face found
                faceCounter = 0 # reset face counter

                faceRectangle = removeOtherFaces(faces, frame) # get the biggest face rectangle (driver's face)

                landmarks = detectFacialLandmarks(faceRectangle) # get facial landmarks

                leftEAR = leftEyeLandmarks(landmarks) # get left eye aspect ratio
                rightEAR = rightEyeLandmarks(landmarks) # get right eye aspect ratio

                drawEyeLandmarks(landmarks) # show eye landmarks on the frame

                EAR = setEyeAspectRatio(leftEAR, rightEAR) # set eye aspect ratio

                TH = setThreshold(EAR) # set an eye openness threshold for the current driver

                detectBlink(leftEAR, rightEAR, EAR, TH, blinkCounter) # detect blink and give alarm if needed

            else: # face not found
               faceCounter += 1 # count number of frames face not found
               txtFile.write('0')
               if faceCounter >= 60: # face not found more than 2 seconds
                   txtFile.write('1')
                   cv2.putText(frame, 'Watch the Road !', (frame.shape[1]/15, frame.shape[0]*9/10),
                       cv2.FONT_HERSHEY_COMPLEX, 0.5, color=(0, 0, 255), thickness=1)

            #out.write(frame)
            #cv2.imshow('display', frame)


        else: # frame is null
            print ('unable to read next frame')
            break

        if cv2.waitKey(1) & 0xFF == 27:   # exit when ESC is pressed
            break

    cap.release()
    cv2.destroyAllWindows()

#process_video("C:\\Users\\Mert\\Dropbox\\ITU\\2017 BITIRME\\DATASETS\\BIG_DATASET\\Training_Evaluation_Dataset\\Training Dataset\\008\\noglasses\\slowBlinkWithNodding (1).avi")