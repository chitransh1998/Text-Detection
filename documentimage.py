import cv2
import numpy as np


#Integrated code for line detection and character segmentation from simple document images

#Read image
img=cv2.imread('best.png')
x=img

#grayscaling
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
cv2.imshow('grayscaling',gray)

#Thresholding the image
thresh = cv2.adaptiveThreshold(gray,200,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2) #thresholding
#cv2.imshow('thresholding',thresh)

#Opening
kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
cv2.imshow('Opening',opening)

#Dilation
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
kernel[0,:]=0;
kernel[4,:]=0;
dilated=cv2.dilate(opening,kernel,iterations=7) #dilate
cv2.imshow("dilated.jpg",dilated) 


#Find the contours
_, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#for each contour we draw a rectangle
for i,contour in enumerate(contours):
    # get rectangle bounding contour
    [x,y,w,h] = cv2.boundingRect(contour)

    # discard areas that are too large
    #if h>300 and w>250:
        #continue
    
    # discard areas that are too small
    if h<20 or w<20:
        continue
    
    # draw rectangle around contour on original image
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)
	
        # Getting ROI
    roi = img[y:y+h, x:x+w]
    # show ROI
    cv2.imwrite('roi_imgs'+str(i)+'.png', roi)
    cv2.imshow('line'+str(i), roi)
    
	#Character detection starts
    img1=roi
    gray=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY) 
    thresh1 = cv2.adaptiveThreshold(gray,200,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2) #thresholding
    kernelo=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    opening1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernelo)
    
    kernel1=cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
    dilated1=cv2.dilate(opening1,kernel1,iterations=5) #dilate
     
    _, contours1, hierarchy = cv2.findContours(dilated1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
    for j,contoure in enumerate(contours1):
      # get rectangle bounding contour
      [x1,y1,w1,h1] = cv2.boundingRect(contoure)

      # discard areas that are too large
      if h>300 and w>250:
        continue
    
      # discard areas that are too small
      if h1<20 or w1<20:
        continue

    
      # draw rectangle around contour on original image
      cv2.rectangle(img1,(x1,y1),(x1+w1,y1+h1),(0,0,255),1)
	
      # Getting ROI
      roi1 = img1[y1:y1+h1, x1:x1+w1]
       # show ROI
      #cv2.imwrite('roi_imgs'+str(i)+'.png', roi)
      cv2.imshow('charachter'+str(j), roi1)
	
	
	

#cv2.imshow("final",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
	
	
	