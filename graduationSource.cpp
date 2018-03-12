#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <dlib/opencv.h>
#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <iostream>
#include <time.h> 

using namespace std;
//using namespace cv;
using namespace dlib;

int main(int argc, char** argv)
{
	cv::VideoCapture cap(0);
	
	if (cap.isOpened()) {		
		cv::Mat frame, grayFrame;		
		std::vector<rectangle> faces;
		frontal_face_detector faceDetector = get_frontal_face_detector();
		shape_predictor pose_model;
		deserialize("C:/dlib-19.9/source/shape_predictor_68_face_landmarks.dat") >> pose_model;
		image_window win;

		for (;;)
		{				
			cap >> frame;
			if (frame.empty()) {
				cout << "frame is empty" << endl;
				break; // end of video stream				
			}
			cv::cvtColor(frame, grayFrame, cv::COLOR_RGB2GRAY);
			cv_image<unsigned char> convertedGray(grayFrame);
			cv_image<rgb_pixel> convertedColor(frame);
            // detect faces
			std::vector<rectangle> faces = faceDetector(convertedGray);

			if (faces.size() != 0) {
				std::vector<full_object_detection> shapes;
				for(unsigned long i = 0; i < faces.size(); ++i)
					shapes.push_back(pose_model(convertedColor, faces[i]));				
				win.clear_overlay();
				win.set_image(convertedColor);
				win.add_overlay(render_face_detections(shapes));
				sleep(30);
				
			}
			else {
				cout << "no face is found" << endl;
				win.clear_overlay();
				win.set_image(convertedColor);
				sleep(30);
			}						

			//cv::imshow("Display window", frame);			
			//if(cv::waitKey(1) == 27) break; // exit when ESC is pressed
		}
		
	}

	else {
		cerr << "Unable to read the file" << endl;
	}
	
	// the camera will be closed automatically upon exit
	// cap.close();
	return 0;
}