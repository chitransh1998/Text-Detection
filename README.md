# Text-Detection
In this project, we utilize various image processing and machine learning algorithms to detect and recognize text in documents and images. Another application area explored was embossed text detction.

# Document Text detection

1. **Documentimage.py**: This is an integrated code for line detection and character segmentation from simple document images.
Usage: `python documentimage.py`
Requirements: opencv,python3,numpy

The algorithm is as follows:

* The image is read and then converted to grayscaled and then adaptive Gaussian thresholding is applied to binarize the image.
*	Opening operation is then applied to denoise the image by using a elliptical structuring element.
*	Dilation is then applies using a horizontal rectangular structuring element (to localize lines)
*	Contours are then drawn in the dilated image.Contours having too large or too small areas are neglected.
*	Each region then contains a line which is further processed for character segmentation.
*	The region of interest containing a text line is then grayscaled and binarized employing adaptive gaussian thresholding.
*	A elliptical structuring element is then used to perform morphological opening operation.
*	Then dilation is performed using a square structuring element.
*	Contours are then drawn across the dilated image.Areas which are too small(Height or width less than 20) and Areas that are too big(Height greater than 300 or width greater than 250) are neglected.
*	Finally,the image obtained contains segmented characters.

![DocumentGUI](https://github.com/chitransh1998/Text-Detection/blob/main/documentgui.png?raw=true)

2. **Livegui.py**: There are three buttons in the GUI viz. Start Webcam,Stop/pause Webcam and Detect Text.

Usage:
*	Live image frames are captured and then converted to grayscale.
*	The grayscale image is then binarized using adaptive Gaussian Mean thresholding.
*	Then it is dilated using a cross kernel of size 3*3.Then median blur is applied to remove noise.
*	Finally contours are detected.Then contours are filtered out if there size is too small (height of width less than 10) or too large(heights or width greater than 100).
*	Finally rectangles are drawn around the filtered contours.

![EmbossedGUI](https://github.com/chitransh1998/Text-Detection/blob/main/embossedgui.png?raw=true)

3. **text_detect.py**: This project aims to detect text regions in images using only image processing techniques with MSER (Maximally Stable Extremal Regions) and SWT (Stroke Width Transform). 

The usage of the code is as follows  

Basic usage is:  
`python text_detect.py -i <input-image>`  

You can give output path   
`python text_detect.py -i images/scenetext01.jpg -o <output-image>`  

More options available  
`python text_detect.py -i images/scenetext01.jpg -o <output-file> -d <light,dark,both,both+> -t`  
Option -i is image path, -o is output path, -d is SWT direction (default is both+), -t option chooses if Tesseract will be used. Normally Tesseract runs poorly if whole image given as input. But I use it for final decision of bounding boxes and it is not required all the time.  

If you want to give whole image to Tesseract to see the impact of the algorithm, try this.  
`python text_detection.py -i images/scenetext01.jpg -f`

For more detail (seeing intermediate steps), the usage given below is also available.  
`python text_detection_detail.py -i images/scenetext01.jpg -d both+ -t`

The working of the code is highlighted as follows:  
* Edge detection is first performed using Canny edge detector.
* MSER regions are then found using the‘getMSERegions’ function.These regions are then colored using ‘colorRegion’ function. 

![Algorithm Steps](https://github.com/chitransh1998/Text-Detection/blob/main/SWT_algo.png?raw=true)

* The different criteria used to filter regions are described in the above image and their respective functions have also been defined.
* Finally the pytesseract tool is used to eliminate the remaining candidate regions to finally get the results.

Results on some images (Text detected in the contour):

![Result1](https://github.com/chitransh1998/Text-Detection/blob/main/detection_result.png?raw=true)

![Result2](https://github.com/chitransh1998/Text-Detection/blob/main/detection_result2.png?raw=true)

