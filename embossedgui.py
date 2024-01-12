#GUI for integrated running of embossed line detection and character segmentation

from PyQt5.QtWidgets import QDialog,QApplication,QFileDialog
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
import cv2
from PyQt5.QtGui import QPixmap, QImage 
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


class Game(QDialog):
  def __init__(self):
     super(Game,self).__init__()
     loadUi('load_image.ui',self)
     self.image=None
     self.show_Image.clicked.connect(self.loadclicked)
     self.save_Button.clicked.connect(self.saveClicked)
     self.detect_Lines.clicked.connect(self.embossedLine)
  @pyqtSlot()
  def embossedLine(self):
     img=self.image
     #grayscaling
     gray=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY) if len(self.image.shape)>=3 else self.image
     #denoising
     denoise1=cv2.fastNlMeansDenoising(gray,15,15,7,21)
     #Unsharp masking for edge enhancement
     gaussian_3 = cv2.GaussianBlur(gray, (9,9), 10.0)
     unsharp_image = cv2.addWeighted(denoise1, 1.5, gaussian_3, -0.5, 0, denoise1)
     #Binarization
     thresh = cv2.adaptiveThreshold(unsharp_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,2)
     #Median blurring
     median = cv2.medianBlur(thresh,7)
     #Horizontal dilation
     kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
     kernel[(0,1,2),:]=0;
     kernel[(4,5,6),:]=0;
     dilated=cv2.dilate(median,kernel,iterations=7)
     #Detecting contours
     p, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
     for i,contour in enumerate(contours):
       area = cv2.contourArea(contour)
       [x,y,w,h] = cv2.boundingRect(contour)
       #Area filtering
       if area>50000 or area<1500:
         continue 
       cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)
       roi = img[y:y+h, x:x+w]
	   
       #Character detection starts in region of image
       graychar=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY) 
       #De noising
       denoise1char =cv2.fastNlMeansDenoising(graychar,15,15,7,21)
       #Unsharp masking
       gaussian_3char = cv2.GaussianBlur(graychar, (9,9), 10.0)
       unsharp_imagechar = cv2.addWeighted(denoise1char, 1.5, gaussian_3char, -0.5, 0, denoise1char)
       #Canny edge detection
       edgeschar=cv2.Canny(unsharp_imagechar,50,150)
       #Binarization
       ret3,threshchar = cv2.threshold(graychar,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
       #Vertical dilation
       kernelchar=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
       kernelchar[:,(0,2)]=0;
       edgeschar = cv2.dilate(edgeschar,kernelchar,iterations = 3)
       #Summation along every column is stored in array t
       t=[]
       row=edgeschar.shape[0]
       col=edgeschar.shape[1]
       sp=[]
       ep=[]
       for i in range(col):
          sum=0
          k=0
          for j in range(row):
              sum=sum+edgeschar[j,i]
              if edgeschar[j,i]>0:
               k=k+1
          t.append(k)
       #Starting points and ending points are found
       n=0
       t=np.array(t)
       stddev=np.std(t)
       mean=np.mean(t)
       stddev=stddev
       diff=mean-stddev
       for i,j in enumerate(t):
         if j<diff:
          t[i]=0

       for i,j in enumerate(t):
        if i>1 and i<(col-1):
           if j>diff and t[i-1]<diff and t[i+1]>diff:
             sp.append(i)
             n=1
           if j>diff and t[i-1]>diff  and t[i+1]<diff and n==1:
             ep.append(i)
             n=0
       if len(sp)!=0:
        w=int(col/len(sp))
       else:
         w=40

       y=2
       h=roi.shape[0]-2
       if len(ep)!=len(sp):

        for i,j in enumerate(sp):
         x=j
         cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,0),1)
         roichar = roi[y:y+h, x:x+w]

       else:

         for i,j in enumerate(sp):
          x=j
          w=ep[i]-sp[i]
          cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,0),1)
          roichar = roi[y:y+h, x:x+w]

       
     img=cv2.resize(img,(200,300))
     self.displayImage(2)
  @pyqtSlot()
  def loadclicked(self):
     fname,filter=QFileDialog.getOpenFileName(self,'Open File','C:\\',"Image Files (*.jpg)")
     if fname:
        self.loadImage(fname)
     else:
        print("Invalid Image")
  @pyqtSlot()
  def saveClicked(self):
     fname,filter=QFileDialog.getSaveFileName(self,'Save File','C:\\',"Image Files (*.jpg)")
     if fname:
        cv2.imwrite(fname,self.image)
     else:
        print('invalid to save')
  def loadImage(self,fname):
     self.image=cv2.imread(fname)
     self.displayImage()
  def displayImage(self,window=1):
     qformat=QImage.Format_Indexed8
	 
     if len(self.image.shape)==3: #rows,columns,channels
         if(self.image.shape[2])==4:
            qformat=QImage.Format_RGBA8888
         else:
            qformat=QImage.Format_RGB888
     img=QImage(self.image,self.image.shape[1],self.image.shape[0],self.image.strides[0],qformat)
     img=img.rgbSwapped()

     if window==1:
        self.original_Image.setPixmap(QPixmap.fromImage(img))
        self.original_Image.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.original_Image.setScaledContents( True )
     if window==2:
        self.processed_Image.setPixmap(QPixmap.fromImage(img))
        self.processed_Image.setScaledContents( True )
        self.processed_Image.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
    
    
 	  
	 
app=QApplication(sys.argv)
window=Game()
window.setWindowTitle('Text detection')
window.show()
sys.exit(app.exec_())