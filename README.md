# AI Engineer Selection Test
Detecting blue water bottles in a plastic bag using OpenCV in Python

### Problem statement
The objective of this test is to find the blue water bottles in a plastic bag in the image and identify them by counting them and display a screenshot. <br />
My approach utilizes OpenCV to perform perspective correction, morphological segmentation, and contour analysis to accurately identify blue bottle caps.<br />

### Prerequisites
You need Python 3.11 installed along with the following libraries:
- opencv-python
- numpy

### Install library using pip
```
pip install -r requirements.txt
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
#### Example output in terminal:
```
Number of bottles detected: 130
```


### Methodology:
#### 1. Perspective Transform
Since the given image is skewed and also consists of border which can be a noise, so perspective transform technique is applied to the input image to adjust camera skew, ensuring the bottles appear top-down and uniformly sized.

#### 2. Preprocessing:
Converts the image to Grayscale to reduce the image from a three-channel (BGR) to a single-channel intensity image. This simplifies the processing pipeline and improves the performance of operations such as thresholding, edge detection, and contour extraction, then apply Median Blur (kernel size 15) to preserve edges while removing noise.

Note!: Have already tried converting the BGR blurred image to HSV color space then use a binary mask to identify pixels within the blue color range and apply the blue mask to the grayscale image to isolate bottle regions, however this step doesn't isolate the caps from blue bottles.

#### 3. Segmentation
Use canny, a popular edge detection detection algorithm, to detect bottle cap edges in images while reducing noise through gradient filtering, which results effectively clearer caps boundaries.

Note!: Have already experimented with Adaptive Gaussian Thresholding to create a binary mask in order to convert from grayscale image into binary (black & white) image. This technique separates bottle caps from the background, handling local lighting variation.


#### 4. Morphological operation:
In this experiment, I examined the image before and after applying morphological operations with varying parameters, such as kernel size and iteration. This process resulted in different sequences of operations that significantly affected the final detection outcome.

According to "Data_Bottles.png" image, morphological operation sequence from the code performs the best, even if there are still noises from the border of image and also from the reflection of the plastic bag that contains blue bottles.

A sequence of Opening, Erosion, Dilation, and Closing is applied to remove small white noise and fill holes inside the bottle caps. <br />
- Erosion works by sliding the kernel across the image. A pixel remains white (255) only if all pixels under the kernel are white, otherwise, it becomes black (0). This reduces object boundaries and removes small white noise.

- Dilation slides the kernel across the image and a pixel becomes white if at least one pixel under the kernel is white. This thickens white regions or objects and fills small holes.
    
- Opening involves erosion followed by dilation in the outer surface (the foreground) of the image.

- Closing involves dilation followed by erosion in the outer surface (the foreground) of the image.

Note!: All operations depend on the size and shape of the kernel and iterations. The kernel is a small matrix that defines the neighborhood for processing each pixel.


#### 5. Detection & Counting:
The result from previous step is the image containing contours with minimized noise which is then used to identify the number of blue bottles in the following steps: 
- Finds Contours on the processed mask.
- Filters: Keeps contours with an area between 150 and 2500 pixels.
- Fitting: Fits an ellipse to the remaining contours to verify the shape.
- Draws the result and displays the count.

### Result
The system will show the number of detected bottles in the terminal and visualizes the result with annotated ellipses.
#### Example output in terminal:
```
Number of bottles detected: 130
```

### Discussion
This system implemented with Traditional OpenCV Technique to achieve blue bottles counting, through edge detection, morphological operation and contour detection. While this approach can count accurately based on "Data_Bottles.png" image, such technique can be struggling when faced with blurred image or inconsistencies in camera positioning, which can ultimately lead to false positive or false negative in counting. So the another way is to use deep-learning approach, such as Single Shot Multibox Detector (SSD) by using pre-trained model to fine-tune on the images to improve robustness and generalization across varying lighting conditions perspectives, and image quality. However, this alternative approach comes with higher computational costs.

### Conclusion
The system successfully detects and counts the majority of blue bottle caps. However, some detected caps appear larger than their actual size due to noise caused by border lighting and reflections on the plastic bag.