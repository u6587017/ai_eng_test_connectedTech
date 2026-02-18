import cv2
import numpy as np
import sys
def count_bottles(image_path):

    # 1. Load Image
    img = cv2.imread(image_path)

    # Perspective Transform
    # Correct perspective distortion so that the plastic bag appears front-facing
    # This ensures that bottle openings are approximately circular instead of skewed
    rows,cols,ch = img.shape

    # Source points (manually selected 4 corners of bag region - top-left(x1,y1), top-right(x2,y2), bottom-left(x3,y3), bottom-right(x4,y4))
    pts1 = np.float32([[230,7],[1160,12],[120,610],[1280,605]])

    # Destination points (transform into square top-down view with width and height of 800 pixels)
    pts2 = np.float32([[0,0],[800,0],[0,800],[800,800]])

    # Compute perspective transform matrix
    M = cv2.getPerspectiveTransform(pts1,pts2)

    # Apply perspective transform to the image
    img = cv2.warpPerspective(img,M,(800,800))

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur the grayscale image to reduce noise and improve edge detection
    # Median blur removes small intensity noise while preserving edges
    # This helps improve adaptive threshold results.
    # From this experiment, median blur with kernel size of 15x15 provides good noise reduction without overly blurring the bottle edges better than GaussianBlur

    # grayBlur = cv2.GaussianBlur(gray, (15,15), 0)
    grayBlur = cv2.medianBlur(gray, 21, 0)

    # Adaptive Threshold separate dark bottle openings from lighter background.
    threshold = cv2.adaptiveThreshold(grayBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
    
    # Canny edge detection to find edges in the blurred grayscale image. The parameters (10,75) are the lower and upper thresholds for hysteresis.
    edges = cv2.Canny(grayBlur,10,75)
    ### Morphology operations
    # Erosion works by sliding the kernel across the image. A pixel remains white (255) only if all pixels under the kernel are white,
    # otherwise, it becomes black (0). This reduces object boundaries and removes small white noise

    # Dilation slides the kernel across the image and a pixel becomes white if at least one pixel under the kernel is white
    # This thickens white regions or objects and fills small holes
    
    # Opening involves erosion followed by dilation in the outer surface (the foreground) of the image
    # Closing involves dilation followed by erosion in the outer surface (the foreground) of the image

    # All operations depend on the size and shape of the kernel and iterations
    # The kernel is a small matrix that defines the neighborhood for processing each pixel

    kernel = np.ones((3,3), np.uint8)
    dilation = cv2.dilate(edges, kernel, iterations=5)

    kernel = np.ones((3,3), np.uint8)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations=5)

    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations=3)

    ## Morphology operations

    # Find contours of the bottles
    result_img = opening.copy()

    # Detect connected regions corresponding to bottle openings
    contours, hierarchy = cv2.findContours(result_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # variable to count number of bottles detected
    counter = 0
    for cnt in contours:
        # Calculate contour area to filter out small noise and large irrelevant contours
        area = cv2.contourArea(cnt)
        if area>150 and area < 2500:
            if len(cnt) >= 5:
                # Fit an ellipse to the contour and draw it on the original image
                ellipse = cv2.fitEllipse(cnt)
                cv2.ellipse(img, ellipse, (0,255,0), 2)
                # Increment bottle counter for each valid contour detected
                counter += 1

    # Display the count of detected bottles on the image and show the results on top left corner
    cv2.putText(img, str(counter), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 2, cv2.LINE_AA)

    # Show the processed images and print the number of bottles detected
    # cv2.imshow('Edges', opening)
    cv2.imshow('Bottles', img)
    cv2.imwrite('counting_result.png', img)
    print(f'Number of bottles detected: {counter}')

    # Wait for a key press and close all OpenCV windows
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = sys.argv[1]
    count_bottles(image_path)