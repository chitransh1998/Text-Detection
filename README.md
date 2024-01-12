# Text-Detection
In this project, we utilize various image processing and machine learning algorithms to detect and recognize text in documents and images. Another application area explored was embossed text detction.

# Document Text detection

1. **Documentimage.py**: This is an integrated code for line detection and character segmentation from simple document images.
Usage: python documentimage.py
Requirements: opencv,python3,numpy

The algorithm is as follows:

●	The image is read and then converted to grayscaled and then adaptive Gaussian thresholding is applied to binarize the image.
●	Opening operation is then applied to denoise the image by using a elliptical structuring element.
●	Dilation is then applies using a horizontal rectangular structuring element (to localize lines)
●	Contours are then drawn in the dilated image.Contours having too large or too small areas are neglected.
●	Each region then contains a line which is further processed for character segmentation.
●	The region of interest containing a text line is then grayscaled and binarized employing adaptive gaussian thresholding.
●	A elliptical structuring element is then used to perform morphological opening operation.
●	Then dilation is performed using a square structuring element.
●	Contours are then drawn across the dilated image.Areas which are too small(Height or width less than 20) and Areas that are too big(Height greater than 300 or width greater than 250) are neglected.
●	Finally,the image obtained contains segmented characters.

2. **Livegui.py**: There are three buttons in the gui viz. Start Webcam,Stop/pause webcam and Detect Text.

Usage:
●	Live image frames are captured and then converted to grayscale.
●	The grayscale image is then binarized using adaptive Gaussian Mean thresholding.
●	Then it is dilated using a cross kernel of size 3*3.Then median blur is applied to remove noise.
●	Finally contours are detected.Then contours are filtered out if there size is too small (height of width less than 10) or too large(heights or width greater than 100).
●	Finally rectangles are drawn around the filtered contours.


