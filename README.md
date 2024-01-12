# Text-Detection
In this project, we utilize various image processing and machine learning algorithms to detect and recognize text in documents and images. Another application area explored was embossed text detction.  
This project was carried out by me as part of the Summer Internship at IIT Delhi in the NVM Research group.

## Document Text detection

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

![Detection_result5](https://github.com/chitransh1998/Text-Detection/blob/main/detection_result5.png?raw=true)

![Detection_result6](https://github.com/chitransh1998/Text-Detection/blob/main/detection_result6.png?raw=true)

## Embossed Text Detection

2. **Livegui.py**: There are three buttons in the GUI viz. Start Webcam,Stop/pause Webcam and Detect Text.

Usage:
*	Live image frames are captured and then converted to grayscale.
*	The grayscale image is then binarized using adaptive Gaussian Mean thresholding.
*	Then it is dilated using a cross kernel of size 3*3.Then median blur is applied to remove noise.
*	Finally contours are detected.Then contours are filtered out if there size is too small (height of width less than 10) or too large(heights or width greater than 100).
*	Finally rectangles are drawn around the filtered contours.

![EmbossedGUI](https://github.com/chitransh1998/Text-Detection/blob/main/embossedgui.png?raw=true)

## Natural Scene Image Text Detection

3. **text_detect.py**: This project aims to detect text regions in **natural scene images** using only image processing techniques with MSER (Maximally Stable Extremal Regions) and SWT (Stroke Width Transform). 

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
  
Image description of the algorithm for Stroke Width Transform :    
![EmbossedGUI](https://github.com/chitransh1998/Text-Detection/blob/main/SWT_algo_images.png?raw=true)  

Results on some images (Text detected in the contour):

![Result1](https://github.com/chitransh1998/Text-Detection/blob/main/detection_result.png?raw=true)

![Result3](https://github.com/chitransh1998/Text-Detection/blob/main/detection_results3.png?raw=true)

![Result4](https://github.com/chitransh1998/Text-Detection/blob/main/detection_results4.png?raw=true)

## Applications
Some possible areas of application for this text detection and character segmentation algorithm are:  

1. Document Digitization: Use text detection to scan and digitize printed documents, making them searchable and editable.
2. Data Entry Automation: Automate data entry tasks by extracting information from forms, invoices, and handwritten records.
3. Language Translation: Identify and translate text in images or documents to make content accessible in different languages.
4. License Plate Recognition (LPR): Recognize license plates on vehicles for traffic management and law enforcement.
5. Text Extraction from Images: Extract textual information from images for indexing and search in content analysis.
6. Handwriting Recognition: Recognize and digitize handwritten text for applications like digitizing notes and postal services.

### References

1.	B. Epshtein, E. Ofek, and Y. Wexler. Detecting text in natural scenes with stroke width transform. In 2010 IEEE Computer Society Conference on Computer Vision and Pattern Recognition, pages 2963–2970, June 2010.
2.	Á. González, L. M. Bergasa, J. J. Yebes, and S. Bronte. Text location in complex images. In Proceedings of the 21st International Conference on Pattern Recognition (ICPR2012), pages 617–620, Nov 2012.
3.	Y. Li and H. Lu. Scene text detection via stroke width. In Proceedings of the 21st International Conference on Pattern Recognition (ICPR2012), pages 681–684, Nov 2012.
4.	Tasneem Wahdan,Gheith A. Abandah,Alisa Seyam,Alaa Awwad Tire type recognition through treads pattern recognition and dot code OCR(ISSN 1992-8424)
5.	S.Sukprasertchai,T. Suesut, Real-time Surface Acquisition of Tire Sidewall for Reading Embossed Information
6.	T.W.Hentzschel,P.Blenkhorn,An optical reading system for embossed Braille characters using a twin shadows approach(Journal of Microcomputer Applications(1995) 18,341-354
7.	Github repository for natural scene image code https://github.com/azmiozgen/text-detection

