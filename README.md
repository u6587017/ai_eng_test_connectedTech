# AI Engineer Selection Test
Detecting multiple bottles using OpenCV in Python

### Objective
The objective of this test is to find the blue water bottles in a plastic bag in the image and identify them by counting them and display a screenshot. <br />
It utilizes OpenCV to perform perspective correction, morphological segmentation, and contour analysis to accurately identify bottle openings.<br />

### Prerequisites
You need Python 3.11 installed along with the following libraries:
- opencv-python (cv2)
- numpy

### Install library using pip
```
pip install -r requirements
```

### Usage
Run the script from the command line by passing the path to your input image as an argument.
#### Syntax:
```
python <script_name>.py <path_to_image>
```
#### Example:
```
python BottleCounter.py Data_Bottles.png
```

The steps I used to achieve this are:
1. Perspective Transform
Since the given image is skewed and also consists of border which can be a noise, so perspective transform technique is is applied to the input image to adjust camera skew, ensuring the bottles appear top-down and uniformly sized.