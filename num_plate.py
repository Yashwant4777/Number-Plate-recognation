# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 16:40:32 2020

@author: Yashwant-Kumar
"""

#imported necessary packages.
import mysql.connector
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'


#creating connection to my databse.
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root123",
  auth_plugin='mysql_native_password',
  database = "num_plate"
)

mycurser = mydb.cursor()


#reading image which is in the same folder.
img = cv2.imread('num11.webp')

#converting BGR image to gray scale as it is easy to find edges in a gray scale image.
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


#Finding the edges using canny edge detection.
canny = cv2.Canny(img_gray,170,255)

#finding the contours of those edges.
contours , hirac = cv2.findContours(canny.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key= cv2.contourArea,reverse = True)[:30]


#iterating through those contours to find the number plate in the image.
for cnt in contours:
    
    #finding the perimeter of each contour.
    perimeter = cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,0.01*perimeter,True)
    if len(approx) == 4:
        cnt_with_plate = approx
        
        #geting the coordinates of the number plate in the image.
        x,y,w,h = cv2.boundingRect(cnt)
        
        #identified the number plate from the image
        num_plate = img_gray[y:y+h,x:x+w]
        break


#applying filters to the number plate to remove any useless information.
num_plate = cv2.bilateralFilter(num_plate,5,17,17)

#seprating the number from the number plate.
thresh , num_plate = cv2.threshold(num_plate,85,255,cv2.THRESH_BINARY)

cv2.imshow('original_img',img)
cv2.imshow('gray_scaled',img_gray)
cv2.imshow('num_plate',num_plate)

#extracting the number from the number plate in the form of text.
num_plate_text = pytesseract.image_to_string(num_plate)


#getting the data from the database.
mycurser.execute("select * from nums")
f=0

#checking whether the car number is matched in our database.
for x in mycurser:
     if(num_plate_text == x[0]):
         print("ENTRY GRANTED!!")
         break
     else:
         f=f+1
if(f==9):
    print("ENTRY DENIED!!")

#closing all windows.
cv2.waitKey(0)
cv2.destroyAllWindows()
