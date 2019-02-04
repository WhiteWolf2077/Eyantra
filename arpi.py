import serial
import numpy as np
import cv2
import cv2.aruco as aruco1
import aruco_lib as aruco
import time
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO


###################################################################################   SETUP    #########
GPIO.setwarnings(False)
camera = PiCamera()       # Picam setup
GPIO.setmode(GPIO.BOARD)  # Setup for PI
#GPIO.setup(3,GPIO.OUT)   # SERVO connection
#pwm = GPIO.PWM(3,50)     # PWM for servo
#pwm.start(0)              # switching it on

Motor1A = 33              # Positive of motor A 
Motor1B = 35              # Negative of motor A
Motor1E = 37              # Pwm for motor A
Motor2A = 36              # Positive of motor B
Motor2B = 38              # Negative of motor B
Motor2E = 40              # Pwm for motor B

GPIO.setup(Motor1A,GPIO.OUT) ####
GPIO.setup(Motor1B,GPIO.OUT) ### MOTOr
GPIO.setup(Motor1E,GPIO.OUT) ### 
GPIO.setup(Motor2A,GPIO.OUT) ####
GPIO.setup(Motor2B,GPIO.OUT) ### CONNECTIONS
GPIO.setup(Motor2E,GPIO.OUT) ####
left = GPIO.PWM(Motor1E, 1000)  ## Value input of Pwm for A
right = GPIO.PWM(Motor2E, 1000) ## Value input of Pwm for B

left.start(0)  ## Duty cycle for A
right.start(0) ## Duty cycle for B
Y = 0 ## Set up the y coordinate

####################################################################################              Function to setup the angle for servo                     ####
def SetAngle(angle):
   duty = angle / 18 + 2
   GPIO.output(3, True)
   pwm.ChangeDutyCycle(duty)
   sleep(1)
   GPIO.output(3, False)
   pwm.ChangeDutyCycle(0)
###############################################################################
################################################################################
###                Function  to implement image capture                      ###
def snap(i):

   camera.start_preview()
   sleep(10)
   camera.capture('/home/pi/Desktop/image'+str(i)+'.jpg')
   
   camera.stop_preview()
   

################################################################################
####             Aruco Detection                                         #######
def aruco_detect(path_to_image,i):

   

   img = cv2.imread(path_to_image)     #give the name of the image with the complete path
   id_aruco_trace = 0
   det_aruco_list = {}
   img2 = img[0:,0:,:]   #separate out the Aruco image from the whole image
   det_aruco_list = aruco.detect_Aruco(img2)
   if det_aruco_list:
     img3 = aruco.mark_Aruco(img2,det_aruco_list)
     id_aruco_trace = aruco.calculate_Robot_State(img3,det_aruco_list)
     for key, value in id_aruco_trace.items():
       print(key,value)
       cv2.imshow('image',img2)
       cv2.waitKey(0)
       cv2.destroyAllWindows()
##################################################################################################################################################################        Main Function  #####
if __name__ == "__main__":
   time.sleep(5) 
   while True:
     ''' For reading the input from arduino '''
     s = serial.Serial("/dev/ttyUSB0",9600)
     t = s.read(1)
     val = str(t).strip("b'").strip("\\n").strip("\\r")
     #print(t)
     print(val)
     ''' MOTOR CONTROL '''
     if (val == 'F'):
       print("Motor in forward direction")
       left.start(25)
       right.start(25)
       GPIO.output(Motor1A,GPIO.LOW)
       GPIO.output(Motor1B,GPIO.HIGH)
       left.ChangeDutyCycle(25)
       GPIO.output(Motor2A,GPIO.LOW)
       GPIO.output(Motor2B,GPIO.HIGH)
       right.ChangeDutyCycle(25)
     if (val == 'L'):
       print("Hard right")
       left.start(25)
       right.start(25)
       GPIO.output(Motor1A,GPIO.LOW)
       GPIO.output(Motor1B,GPIO.HIGH)
       left.ChangeDutyCycle(35)
       GPIO.output(Motor2A,GPIO.LOW)
       GPIO.output(Motor2B,GPIO.HIGH)
       right.ChangeDutyCycle(25)
     if (val == 'l'):
       print("Soft right")
       left.start(25)
       right.start(25)
       GPIO.output(Motor1A,GPIO.LOW)
       GPIO.output(Motor1B,GPIO.HIGH)
       left.ChangeDutyCycle(30)
       GPIO.output(Motor2A,GPIO.LOW)
       GPIO.output(Motor2B,GPIO.HIGH)
       right.ChangeDutyCycle(25)
     if (val == 'R'):
       print("Hard left")
       left.start(25)
       right.start(25)
       GPIO.output(Motor1A,GPIO.LOW)
       GPIO.output(Motor1B,GPIO.HIGH)
       left.ChangeDutyCycle(25)
       GPIO.output(Motor2A,GPIO.LOW)
       GPIO.output(Motor2B,GPIO.HIGH)
       right.ChangeDutyCycle(35)
     if (val == 'r'):
       print("Soft left")
       left.start(25)
       right.start(25)
       GPIO.output(Motor1A,GPIO.LOW)
       GPIO.output(Motor1B,GPIO.HIGH)
       left.ChangeDutyCycle(25)
       GPIO.output(Motor2A,GPIO.LOW)
       GPIO.output(Motor2B,GPIO.HIGH)
       right.ChangeDutyCycle(30)
     if (val == 'v'):
       
       continue

     if (val == 'S'):
       if (Y==0 or Y==1 ):
         Y = Y+1  
         print("Motor in forward direction")
         left.start(25)
         right.start(25)
         GPIO.output(Motor1A,GPIO.LOW)
         GPIO.output(Motor1B,GPIO.HIGH)
         left.ChangeDutyCycle(30)
         GPIO.output(Motor2A,GPIO.LOW)
         GPIO.output(Motor2B,GPIO.HIGH)
         right.ChangeDutyCycle(25)
         print(Y)
         sleep(0.8)   
            
       if (Y == 2 ):
         print("Stop")
         print(Y)
         left.start(0)
         right.start(0)
         GPIO.output(Motor1A,GPIO.LOW)
         GPIO.output(Motor1B,GPIO.HIGH)
         left.ChangeDutyCycle(0)
         GPIO.output(Motor2A,GPIO.LOW)
         GPIO.output(Motor2B,GPIO.HIGH)
         right.ChangeDutyCycle(0)
         
         '''for i in range(1,2):
           SetAngle(i*45)
           snap(i)
           aruco_detect('/home/pi/Desktop/image'+str(i)'.jpg')
           fo = open("eYRC#AB#183.csv", "a")
           fo.write('SIM '+str(i-1)+","+"Detected")
           fo.close()'''
             
         left.start(25)
         right.start(25)
         GPIO.output(Motor1A,GPIO.LOW)
         GPIO.output(Motor1B,GPIO.HIGH)
         left.ChangeDutyCycle(50)
         GPIO.output(Motor2A,GPIO.HIGH)
         GPIO.output(Motor2B,GPIO.LOW)
         right.ChangeDutyCycle(50)
        
     
GPIO.cleanup()  
