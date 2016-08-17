//THIS CODE PRODUCES AN EXECUTABLE THAT CAN BE CALLED FROM THE PROGRAM priorStagePattern.py 
//USED TO CAPTURE IMAGES FROM THE AMSCOPE MU500 CAMERA AND SAVE IMAGES TO NUMBERED FILES


#include <iostream> //standard includes
#include <time.h>
#include <string.h>
#include <vector>
#include <stdio.h>
#include <fstream>
#include <sstream>
#include <istream>
#include <stdlib.h>

#include "opencv/cv.h" //these are all included from OpenCV
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/core.hpp"
#include "opencv2/opencv.hpp"
#include "opencv2/imgcodecs.hpp"

using namespace std; //standard
using namespace cv; //OpenCV

int main(int argc, char *argv[]) {
	string input; //input from amscopeCam.py is of type string
	cin >> input; //get input from stdin PIPE in amscopeCam.py

	int frameWidth = 2592;
	int frameHeight = 1944;

	VideoCapture cap(0); //argument is zero which means "choose the first/only camera available"
	
	if (!cap.isOpened()) //is the camera can't open or can't find camera
			return -1;

	Mat frame; //initialize frame as a Mat
	cap.set(CAP_PROP_FPS, 35); //set frames per second
	cap.set(CAP_PROP_FRAME_WIDTH, 2592); //essentially setting resolution
	cap.set(CAP_PROP_FRAME_HEIGHT, 1944);
	
	cap.grab(); //grab image and put it in cap

	cap >> frame; //put image from cap into frame = change from VideoCapture to Mat (must be Mat to save image)

	ostringstream fn; //ostringsteam can operate on strings
	fn << "Images/img" << input << ".png"; //put the image number (input) from amscopeCam.py into filename
	                                       //the location "Images/" might have to be modified

	imwrite(fn.str(), frame); //write each image (frame) to a new file
}


