# AI Engineer Selection Test
Detecting multiple bottles using OpenCV in Python

### Objective
The objective of this test is to find the blue water bottles in a plastic bag in the image and identify them by counting them and display a screenshot. <br />
It utilizes OpenCV to perform perspective correction, morphological segmentation, and contour analysis to accurately identify bottle openings.<br />

The steps I used to achieve this are:
1. Perspective Transform
Since the given image is skewed and also consists of border which can be a noise, so perspective transform technique is is applied to the input image to adjust camera skew, ensuring the bottles appear top-down and uniformly sized.