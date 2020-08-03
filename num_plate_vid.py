# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 18:30:57 2020

@author: Yashwant-Kumar
"""

#imported necessary packages.
import mysql.connector
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'


#creating connection to my databse.
mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "root123",
        auth_plugin='mysql_native_password',
        database = "vid_num_plate"
        )

mycurser = mydb.cursor(buffered=True)


#reading video which is in the same folder.
cap = cv2.VideoCapture('6.mp4')

#getting the frames from video.
ret,frame1 = cap.read()
ret,frame2 = cap.read()
ret1 = True


while cap.isOpened():
    
    if(ret1 == True):
        
        #finding the difference between each frame.
        diff = cv2.absdiff(frame1,frame2)
        
        #converting the frame to gray scale.
        im_gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(im_gray,(5,5),0)
        _,thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
        #it helps to remove the useless information or background distrubance.
        dilate = cv2.dilate(thresh,None,iterations=5)
        
        #finding the contours.
        contour,_ = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contour:
            
            #finding the coordinates of each contour found.
            x,y,w,h = cv2.boundingRect(cnt)
            
            #trying to find the car in each frame by finding the area of each contour.
            if(cv2.contourArea(cnt)>=19000 and cv2.contourArea(cnt)<=24000):
                
                
                frame_gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
                
                #Finding the edges using canny edge detection.
                canny = cv2.Canny(frame_gray,170,255)
                
                contours,_ = cv2.findContours(canny.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
                contours = sorted(contours, key= cv2.contourArea,reverse = True)[:35]
                
                #iterating through those contours to find the number plate in the frame.
                for cnt in contours:
                    
                    perimeter = cv2.arcLength(cnt,True)
                    approx = cv2.approxPolyDP(cnt,0.01*perimeter,True)
                    if len(approx) == 4:
                        cnt_with_plate = approx
                        #geting the coordinates of the number plate in the frame
                        x,y,w,h = cv2.boundingRect(cnt)
                        break
                    
                #applying filters to the number plate to remove any useless information.
                num_plate = cv2.bilateralFilter(frame_gray[y:y+h,x:x+w],5,17,17)
                thresh , num_plate = cv2.threshold(num_plate,95,255,cv2.THRESH_BINARY)
                
                cv2.imshow('res',num_plate)
                #extracting the number from the number plate in the form of text.
                num_plate_text = pytesseract.image_to_string(num_plate)
                
                #getting the data from the database.
                mycurser.execute("select * from vid_nums")
                
                #using as a flag
                f=0
                #checking whether the car number is matched in our database.
                for x in mycurser:
                     if(num_plate_text == x[0]):
                         f=1
                         print("ENTRY GRANTED!!")
                         cv2.destroyAllWindows()    
                         cap.release()
                         break
                if(f==1):
                    break
        frame1 = frame2
        
        #reading frames.
        ret1,frame2 = cap.read()
        cv2.waitKey(20)
        
    
    elif(ret1 == False):
        print("ENTRY DENIED!!")
        cv2.destroyAllWindows()    
        cap.release()
        break
    
