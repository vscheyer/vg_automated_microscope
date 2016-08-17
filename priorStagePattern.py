import time 
import serial 
import subprocess
from subprocess import *  #used in pattern to run camera_vg_take2.exe
import os

 
# configure the serial connections (the parameters differs on the device you are connecting to) 
ser = serial.Serial( 
    port='COM3',
    baudrate=9600, 
    parity=serial.PARITY_ODD, #I honestly don't know what lines 12, 13, 14 do, they were just in the code we started with...
    stopbits=serial.STOPBITS_TWO, 
    bytesize=serial.SEVENBITS 
) 
 
 
print ("opening port") 
if ser.isOpen() is not True: 
    print ("...port is not open...") 
    exit 
 
 
print ('Follow the setup instructions.\nInsert "exit" to leave the application.')

#cmd = str.encode('H\r\n') 

in1 = "JXD -1" #changes correlation between joystick direction and stage's X axis direction of movement'--use "JYD" to change Y axis 
ser.write(cmd) #write/send command to stage controller thru serial
time.sleep(1) #give ser a second to get command


def pattern(imageX, imageY, columns, rows, imgX, imgY): # this function is called after the setup (below)--it snakes stage back and forth
	cmd = str.encode('H\r\n') #H disables joystick so user won't interrupt pattern
	ser.write(cmd) 

	ser.reset_output_buffer() #make sure serial is cleared
	ser.reset_input_buffer()
	time.sleep(1)

	imgNum = 1 #initialize the counting system for labeling image files

	for x in range (0, int(rows) + 1): #rows --- add "+1" to ensure none of sample is missed (since rows could be a decimal)
		for x in range (0, int(columns) + 1): #columns ||| 

			time.sleep(1)

			imgStr = str(imgNum) #convert the imgNum to string so it can be passed in the stdin PIPE

			#"exe" refers to the c++ executable "camera_vg_take2.exe"
			#subprocess.Popen runs the c++ exe as a separate thread, stdin=PIPE opens a pipe to send input to exe

			p = subprocess.Popen("camera_vg_take2.exe", stdin = PIPE, universal_newlines = True) #universal_newlines means stdin can be a string, not bytes
			p.communicate(imgStr) #communicate--sends the imgStr through stdin PIPE so exe can label image file 

			time.sleep(2) #wait to ensure that exe is done saving image

			imgNum += 1 #update the image number so that most recent img file doesn't get overwritten

			cmd = str.encode('L ' + str(imgX) + '\r\n') #"L" tells the stage to move left by imgX number of steps--need space between L and imgX
			ser.write(cmd) 
			time.sleep(2)

		time.sleep(1)

		inmStr = str(imgNum)

		p = subprocess.Popen("camera_vg_take2.exe", stdin=PIPE, shell=True, universal_newlines=True) #same as above
		p.stdin.write(imgStr)
		time.sleep(2)

		imgNum += 1

		cmd = str.encode('B ' + str(imgY) + '\r\n') #"B" tells stage to move back by imgY number of steps
		ser.write(cmd) 
		time.sleep(1)
		imgX = imgX * -1 #this changes the sign of imgX so that next time thru loop stage moves (negative L) = R


in1 = "J"
cmd = str.encode(in1 + '\r\n') #"J" activates the joystick 
ser.write(cmd) 
time.sleep(1)

print("Use the joystick to go to the end position of the pattern.") #end should be lower right corner of physical slide, upper right of camera image of slide

in1 = input("Type \"end\" position or just press enter:") #"end" moves stage to automatic end position (good when testing repeatedly)
if in1 == 'exit': #type exit to exit out of program
    ser.close() 
    exit()
if in1 == 'end':
	cmd = str.encode('G -6938 -13940\r\n') #"G x y" means "go to " (x, y)--these x and y coordinates can be changed for different automatic "end" position
	ser.write(cmd) 
	time.sleep(1) 

in1 = input("Enter PX: ")	#operator should literally type "px" (NOT cap sensitive)
cmd = str.encode(in1 + '\r\n') #"PX" means "get the current x coordinate of stage"
ser.reset_input_buffer() #clear the buffer so controller can get command
ser.write(cmd)
out = str.encode('') #initialize out variable to store controller's return later
time.sleep(2)
while ser.inWaiting() > 0: #wait for serial to reply
	out += ser.read(1).strip() #read whatever the controller returns (px = x position) and strip
print ("End position x: " + str(out))
	
endX = int(out.strip()) #store the x position in int variable (for use in calculations)


in1 = input("Enter PY: ") #operator should type "py"
if in1 == 'exit': 
   	ser.close() 
   	exit()
cmd = str.encode(in1 + '\r\n') #"PY" means "get the current y coordinate of stage"
ser.write(cmd)
out = str.encode('')
time.sleep(1)
while ser.inWaiting() > 0:
	out += ser.read(1) 
print ("End position y: " + str(out))

endY = int(out.strip())


print("Use the joystick to go to the start of the pattern.") #should be upper left corner of physical slide, lower left corner of camera image


in1 = input("Type \"start\" or just press enter: ") #"start" moves stage to a set position (good when testing repeatedly)
if in1 == 'exit': 
	ser.close() 
	exit()
if in1 == 'start':                               #This section is same as above, now for starting position
	cmd = str.encode('G 10436 3621\r\n') 
	ser.write(cmd) 
	time.sleep(1) 
in1 = input("Enter PX: ")
cmd = str.encode(in1 + '\r\n') 
ser.reset_input_buffer()
ser.write(cmd) 
out = str.encode('')
time.sleep(1)
while ser.inWaiting() > 0: 
	out += ser.read(1)
print ("Starting position x: ")
print (str(out))

startX = int(out.strip())


in1 = input("Enter PY: ") #get starting y position:
if in1 == 'exit': 
	ser.close() 
	exit()
cmd = str.encode(in1 + '\r\n') 
ser.write(cmd) 
out = str.encode('') 
time.sleep(1) 
while ser.inWaiting() > 0: 
	out += ser.read(1) 
print ("Starting y position: \n" + str(out))

startY = int(out.strip())

patternX = abs(endX - startX) #patternX is the size of the wholel slide/pattern X length
patternY = abs(endY - startY) #patternY is the size of the whole slide/pattern Y height

imageX = 1140 #number of stage steps for image's X length
imageXstr = str(1140) 
imageY = 2000 #number of stage steps for image's Y height
imageYstr = str(845)

columns = patternX/imageX #calculate the number of columns the slide is to be divided into
rows = patternY/imageY #calculate number of rows

print(str(patternX) + " " + str(patternY) + "\n" + str(columns) + " " + str(rows)) #this is optional--lets user see the values

time.sleep(1)

pattern(imageX, imageY, columns, rows, imageX, imageY) #calls the "pattern" function (written above)

in1 = "J" #activates the joystick after the pattern finishes (since pattern deactivates it)
cmd = str.encode(in1 + '\r\n') 
ser.write(cmd) 
time.sleep(1)