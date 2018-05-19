import numpy as np
import cv2
#import winsound
import dlib

# load cascades
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('C:\\Python27\\Lib\\site-packages\\dlib\\shape_predictor_68_face_landmarks.dat')

inputName = 'test_video'
txtFile = open(inputName+'.txt', 'a')
counter=0
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter(fileName+'_output.avi', fourcc, 30.0, (640, 480))

# play sound
#FREQ = 2500
#DURATION = 200  # in miliseconds

cap = cv2.VideoCapture('C:\\Users\\Mert\\Documents\\GitHub\\Drowsy_Driver_Detection\\Eye_Cropper\\test_video.avi')
# ('C:\\Users\\Itouch\\Desktop\\burakDrive1.avi')

# set counters to measure number of frames
blinkCounter = 0
faceCounter = 0

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    if frame is not None:
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to grayscale
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

               #frame = cv2.rectangle(grayFrame, (x, y), (x + w, y + h), (255, 0, 0), 1) # put rectangle around face
               detected_landmarks = shape_predictor(grayFrame, d).parts()  # detect landmarks

           landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])  # extract landmark coordinates

           left_eye_y_center = (landmarks[42][0, 1] + landmarks[43][0, 1] + landmarks[44][0, 1] + landmarks[45][0, 1] + landmarks[46][0, 1] + landmarks[47][0, 1]) / 6
           left_eye_x_center = (landmarks[42][0, 0] + landmarks[43][0, 0] + landmarks[44][0, 0] + landmarks[45][0, 0] + landmarks[46][0, 0] + landmarks[47][0, 0]) / 6

           right_eye_y_center = (landmarks[36][0, 1] + landmarks[37][0, 1] + landmarks[38][0, 1] + landmarks[39][0, 1] + landmarks[40][0, 1] + landmarks[41][0, 1]) / 6
           right_eye_x_center = (landmarks[36][0, 0] + landmarks[37][0, 0] + landmarks[38][0, 0] + landmarks[39][0, 0] + landmarks[40][0, 0] + landmarks[41][0, 0]) / 6

           box_radius=landmarks[39][0, 0]-landmarks[36][0, 0];

           #cv2.rectangle(grayFrame, (left_eye_x_center - box_radius, left_eye_y_center - box_radius),
                                    # (left_eye_x_center + box_radius, left_eye_y_center + box_radius), (255, 0, 0), 1) #Mark the left eye region

           left_eye_box = grayFrame[(left_eye_y_center - box_radius):(left_eye_y_center + box_radius),
                          (left_eye_x_center - box_radius):(left_eye_x_center + box_radius)]


           #cv2.rectangle(grayFrame, (right_eye_x_center - box_radius, right_eye_y_center - box_radius),
                                    # (right_eye_x_center + box_radius, right_eye_y_center + box_radius), (255, 0, 0), 1) #Mark the right eye region

           right_eye_box = grayFrame[(right_eye_y_center - box_radius):(right_eye_y_center + box_radius),
                           (right_eye_x_center - box_radius):(right_eye_x_center + box_radius)]



           for idx, point in enumerate(landmarks):
               if 35 < idx and idx < 48:
                   pos = (point[0, 0], point[0, 1])
                   # draw points on the landmark positions
                   #cv2.circle(grayFrame, pos, 1, color=(0, 255, 255))
                   # eyes points are from 12 to 47
        else:
            #trust the latest known position
            left_eye_x_center=left_eye_x_center
            right_eye_x_center=right_eye_x_center
            left_eye_y_center=left_eye_y_center
            right_eye_y_center=right_eye_y_center
            box_radius=box_radius

            #cv2.rectangle(grayFrame, (left_eye_x_center - box_radius, left_eye_y_center - box_radius),
                                  #    (left_eye_x_center + box_radius, left_eye_y_center + box_radius), (255, 0, 0),1)  # Mark the left eye region

            left_eye_box = grayFrame[(left_eye_y_center - box_radius):(left_eye_y_center + box_radius),
                           (left_eye_x_center - box_radius):(left_eye_x_center + box_radius)]  # Crop the left eye region


            #cv2.rectangle(grayFrame, (right_eye_x_center - box_radius, right_eye_y_center - box_radius),
                                 #     (right_eye_x_center + box_radius, right_eye_y_center + box_radius), (255, 0, 0), 1)  # Mark the right eye region

            right_eye_box = grayFrame[(right_eye_y_center - box_radius):(right_eye_y_center + box_radius),
                            (right_eye_x_center - box_radius):(right_eye_x_center + box_radius)]  # Crop the left eye region



        #out.write(frame)
        #cv2.imshow('display', left_eye_box)

    else:
        print ('unable to read next frame')
        break

    #resized_left_eye_box = cv2.resize(left_eye_box, (24, 24))
    #resized_right_eye_box = cv2.resize(right_eye_box, (24, 24))
    resized_left_eye_box = cv2.resize(left_eye_box, (24, 24))
    cv2.imwrite('BMG'+str(counter)+'.jpg', resized_left_eye_box)
    counter=counter+1;
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

