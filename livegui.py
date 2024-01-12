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
     loadUi('Livegui.ui',self)
     self.image=None
     self.processedImage=None
     self.startButton.clicked.connect(self.start_webcam)
     self.stopButton.clicked.connect(self.stop_webcam)
     self.textButton.toggled.connect(self.text_webcam) 
     self.textButton.setCheckable(True)
     self.canny_Enabled=False
	 
  def text_webcam(self,status):
      if status:
         self.canny_Enabled=True
         self.textButton.setText('Text Detection stop')
      else:
         self.canny_Enabled=False
         self.textButton.setText('Text detect start')
  
  def start_webcam(self):
     self.capture=cv2.VideoCapture(0)
     self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,191)
     self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,641)

     self.timer=QtCore.QTimer(self)
     self.timer.timeout.connect(self.update_frame)
     self.timer.start(5)

  def update_frame(self):
     ret,self.image=self.capture.read()
     self.image=cv2.flip(self.image,1)
     self.displayImage(self.image,1)

     if(self.canny_Enabled):
         gray=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY) if len(self.image.shape)>=3 else self.image
         thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,12)
         kernel=cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
         dilated=cv2.dilate(thresh,kernel,iterations=2)
         medianblur= cv2.medianBlur(dilated,11)
         _, contours, hierarchy = cv2.findContours(medianblur,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
         for contour in contours:
           [x,y,w,h] = cv2.boundingRect(contour)
           if h>100 and w>100:
            continue
           if h<10 or w<10:
            continue
           cv2.rectangle(self.image,(x,y),(x+w,y+h),(255,0,255),2)
         self.processedImage=self.image
         self.displayImage(self.processedImage,2)

  def displayImage(self,img,window=1):
     qformat=QImage.Format_Indexed8
     if len(img.shape)==3:
       if img.shape[2]==4: #extra channel alpha for transparency
          qformat=QImage.Format_RGBA8888
       else:
           qformat=QImage.Format_RGB888
     outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
     outImage=outImage.rgbSwapped()
	 
     if window==1:
        self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
        self.imgLabel.setScaledContents(True)
     if window==2:
        self.processedLabel.setPixmap(QPixmap.fromImage(outImage))
        self.processedLabel.setScaledContents(True)
		
		
  def stop_webcam(self):
      self.timer.stop()
     
	  
	  
	  
if __name__=='__main__':
    app=QApplication(sys.argv)
    window=Game()
    window.setWindowTitle('Live Text detection')
    window.show()
    sys.exit(app.exec_())