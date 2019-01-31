# -*- coding: utf-8 -*-
"""
**************************************************************************
*                  E-Yantra Robotics Competition
*                  ================================
*  This software is intended to check version compatiability of open source software
*  Theme: ANT BOT
*  MODULE: Task1.2
*  Filen:me: Task1.2.py
*  Version: 1.0.0  
*  Date: October 31, 2018
*  
*  Author: e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
**************************************************************************
"""

"""
ArUco ID Dictionaries: 4X4 = 4-bit pixel, 4X4_50 = 50 combinations of a 4-bit pixel image
List of Dictionaries in OpenCV's ArUco library:
DICT_4X4_50	 
DICT_4X4_100	 
DICT_4X4_250	 
DICT_4X4_1000	 
DICT_5X5_50	 
DICT_5X5_100	 
DICT_5X5_250	 
DICT_5X5_1000	 
DICT_6X6_50	 
DICT_6X6_100	 
DICT_6X6_250	 
DICT_6X6_1000	 
DICT_7X7_50	 
DICT_7X7_100	 
DICT_7X7_250	 
DICT_7X7_1000	 
DICT_ARUCO_ORIGINAL

Reference: http://hackage.haskell.org/package/opencv-extra-0.2.0.1/docs/OpenCV-Extra-ArUco.html
Reference: https://docs.opencv.org/3.4.2/d9/d6a/group__aruco.html#gaf5d7e909fe8ff2ad2108e354669ecd17
"""

import numpy as np
import imutils
import cv2
import cv2.aruco as aruco1
import aruco_lib as aruco
import time
def aruco_detect(path_to_image,shape1,color1,shape2,color2,i):
    '''
    you will need to modify the ArUco library's API using the dictionary in it to the respective
    one from the list above in the aruco_lib.py. This API's line is the only line of code you are
    allowed to modify in aruco_lib.py!!!
    '''
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
        '''
        Code for triggering color detection on ID detected
        ''' 
        color_detect(img2,shape1,color1,shape2,color2,i,key)
        cv2.destroyAllWindows()

def color_detect(img,shape1,color1,shape2,color2,i,key):
    '''
    code for color Image processing to detect the color and shape of the 2 objects at max.
    mentioned in the Task_Description document. Save the resulting images with the shape
    and color detected highlighted by boundary mentioned in the Task_Description document.
    The resulting image should be saved as a jpg. The boundary should be of 25 pixels wide.

    '''
    

    lower_range_blue = np.array([100, 0, 0])
    upper_range_blue = np.array([255,150,150])

    lower_range_green = np.array([0, 100, 0])
    upper_range_green = np.array([100, 255, 100])

    lower_range_red = np.array([0, 0, 100])
    upper_range_red = np.array([100, 100, 255])

    mask_blue = cv2.inRange(img, lower_range_blue, upper_range_blue)
    mask_green = cv2.inRange(img, lower_range_green, upper_range_green)
    mask_red = cv2.inRange(img, lower_range_red, upper_range_red)
    kernel = np.ones((5,5), np.uint8)
    erosion_blue = cv2.erode(mask_blue,kernel,iterations = 2)
    erosion_red = cv2.erode(mask_red,kernel,iterations = 2)
    erosion_green = cv2.erode(mask_green,kernel,iterations = 2)
    opening_blue = cv2.dilate(erosion_blue, kernel,iterations = 2)
    opening_red = cv2.dilate(erosion_red, kernel,iterations = 2)
    opening_green = cv2.dilate(erosion_green, kernel,iterations = 2)
    
    #erosion = cv2.erode(mask,kernel,iterations = 1)
    #erosion = cv2.erode(mask,kernel,iterations = 1)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred_green = cv2.GaussianBlur(opening_green, (5, 5), 0)
    blurred_blue = cv2.GaussianBlur(opening_blue, (5, 5), 0)
    blurred_red = cv2.GaussianBlur(opening_red, (5, 5), 0)
    _,thresh_blue = cv2.threshold(blurred_blue, 200, 255, cv2.THRESH_BINARY)
    _,thresh_green = cv2.threshold(blurred_green, 200, 255, cv2.THRESH_BINARY)
    _,thresh_red = cv2.threshold(blurred_red, 200, 255, cv2.THRESH_BINARY)
    
    x2 = '-'
    y2 = '-'
    x1 = '-'
    y1 = '-'


    if color1 == 'green' :  
       contours = cv2.findContours(thresh_green,1,2)
       contours = contours[0] if imutils.is_cv2() else contours[1]
       for c in contours:
          M = cv2.moments(c)

          cX = int(M["m10"] / M["m00"])
          cY = int(M["m01"] / M["m00"])
          approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
          #print (len(approx))
          
          if len(approx)==3: 
              
              if shape1 == 'triangle':
                 cv2.drawContours(img,[c],-1,(255,0,0),25)
                 x1 = cX
                 y1 = cY
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
          elif len(approx)==4: 
              
              if shape1 == 'square':
                 x1 = cX
                 y1 = cY
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                 cv2.drawContours(img,[c],-1,(255,0,0),25)
          elif len(approx)>15:
              
              if shape1 == 'circle':
                 x1 = cX
                 y1 = cY
                 cv2.drawContours(img,[c],-1,(255,0,0),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
###############################################################################################################################################


    if color1 == 'blue':  
       contours = cv2.findContours(thresh_blue,1,2)
       contours = contours[0] if imutils.is_cv2() else contours[1]
       for c in contours:
          M = cv2.moments(c)
          cX = int(M["m10"] / M["m00"])
          cY = int(M["m01"] / M["m00"])
          approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
          #print (len(approx))
          
          if len(approx)==3: 
             
              if shape1 == 'triangle':
                 x1 = cX
                 y1 = cY
                 cv2.drawContours(img,[c],-1,(0,0,255),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
          elif len(approx)==4: 
              
              if shape1 == 'square':
                 x1 = cX
                 y1 = cY
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                 cv2.drawContours(img,[c],-1,(0,0,255),25)
          elif len(approx)>15:
              
              if shape1 == 'circle':
                 x1 = cX
                 y1 = cY
                 cv2.drawContours(img,[c],-1,(0,0,255),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

###############################################################################################################################################


    if color1 == 'red':  
       contours = cv2.findContours(thresh_red,1,2)
       contours = contours[0] if imutils.is_cv2() else contours[1]
       for c in contours:
          M = cv2.moments(c)
          cX = int(M["m10"] / M["m00"])
          cY = int(M["m01"] / M["m00"])
          approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
          #print (len(approx))
          
          if len(approx)==3: 
              
              if shape1 == 'triangle':
                 x1 = cX
                 y1 = cY
                 cv2.drawContours(img,[c],-1,(0,255,0),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
          elif len(approx)==4: 
              
              if shape1 == 'square':
                 x1 = cX
                 y1 = cY
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                 cv2.drawContours(img,[c],-1,(0,255,0),25)
          elif len(approx)>15:
              
              if shape1 == 'circle':

                 x1 = cX
                 y1 = cY
                 cv2.drawContours(img,[c],-1,(0,255,0),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


    if color2 == 'green' :  
       contours = cv2.findContours(thresh_green,1,2)
       contours = contours[0] if imutils.is_cv2() else contours[1]
       for c in contours:
          M = cv2.moments(c)
          cX = int(M["m10"] / M["m00"])
          cY = int(M["m01"] / M["m00"])
          approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
          #print (len(approx))
          
          if len(approx)==3: 
              
              if shape2 == 'triangle':
                 x2 = cX
                 y2 = cY
                 cv2.drawContours(img,[c],-1,(255,0,0),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
          elif len(approx)==4: 
              
              if shape2 == 'square':
                 x2 = cX
                 y2 = cY
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                 cv2.drawContours(img,[c],-1,(255,0,0),25)
          elif len(approx)>15:
              
              if shape2 == 'circle':
                 x2 = cX
                 y2 = cY
                 cv2.drawContours(img,[c],-1,(255,0,0),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
###############################################################################################################################################


    if color2 == 'blue':  
       contours = cv2.findContours(thresh_blue,1,2)
       contours = contours[0] if imutils.is_cv2() else contours[1]
       for c in contours:
          M = cv2.moments(c)
          cX = int(M["m10"] / M["m00"])
          cY = int(M["m01"] / M["m00"])
          approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
          #print (len(approx))
          
          if len(approx)==3: 
              
              if shape2 == 'triangle':
                 x2 = cX
                 y2 = cY
                 cv2.drawContours(img,[c],-1,(0,0,255),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
          elif len(approx)==4: 
              
              if shape2 == 'square':
                 x2 = cX
                 y2 = cY
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                 cv2.drawContours(img,[c],-1,(0,0,255),25)
          elif len(approx)>15:
              
              if shape2 == 'circle':
                 x2 = cX
                 y2 = cY
                 cv2.drawContours(img,[c],-1,(0,0,255),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

###############################################################################################################################################


    if color2 == 'red':  
       contours = cv2.findContours(thresh_red,1,2)
       contours = contours[0] if imutils.is_cv2() else contours[1]
       for c in contours:
          M = cv2.moments(c)
          cX = int(M["m10"] / M["m00"])
          cY = int(M["m01"] / M["m00"])
          approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
          #print (len(approx))
          
          if len(approx)==3: 
              
              if shape2 == 'triangle':
                 x2 = cX
                 y2 = cY
                 cv2.drawContours(img,[c],-1,(0,255,0),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
          elif len(approx)==4: 
              
              if shape2 == 'square':
                 x2 = cX
                 y2= cY
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                 cv2.drawContours(img,[c],-1,(0,255,0),25)
          elif len(approx)>15:
              
              if shape2 == 'circle':
                 x2 = cX
                 y2 = cY
                 cv2.drawContours(img,[c],-1,(0,255,0),25)
                 cv2.putText(img, str(cX)+','+str(cY), (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

   
    fo = open("183_Task1.2.csv", "a")
    
    fo.write('ArUco'+str(i)+'.jpg'+","+str(key)+","+"("+str(x1)+'-'+str(y1)+")"+","+"("+str(x2)+'-'+str(y2)+")"+"\n")
    fo.close()
    pass



    cv2.imshow("ColorImage",img)
    cv2.imwrite('ArUco'+str(i)+'.jpg',img)
    cv2.waitKey(0)

	

if __name__ == "__main__":    
    #aruco_detect('Image1.jpg')
    #aruco_detect('Image2.jpg')
    #aruco_detect('Image3.jpg')
    #aruco_detect('Image4.jpg')
    #aruco_detect('Image5.jpg')
    fo = open("183_Task1.2.csv", "w+")
    fo.write('Image Name'+','+'ArUco ID'+','+"(x-y Object-1)"+','+"(x-y Object-2)"+"\n")
    fo.close()
    pass
    print('Shapes available:\n 1.circle\n 2.square\n 3.rectangle\n 4.none')
    print('Colors available:\n 1.red\n 2.green\n 3.blue\n 4.none')
    i=1
    while(1):
            
            print('Enter path of image : ')
            image = input()
            print('Enter the shape number 1')
            shape1 = input()
            print('Enter the color of the shape1')
            color1 = input()
            print('Enter the shape number 2')
            shape2 = input()
            print('Enter the color of the shape2')
            color2 = input()
            
            aruco_detect(image,shape1,color1,shape2,color2,i)
            i=i+1
            print('Press q to quit :')
            quit = input()
            if quit == 'q': 
                   break
