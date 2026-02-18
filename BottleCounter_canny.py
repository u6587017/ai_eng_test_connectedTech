import cv2
import numpy as np
img = cv2.imread('./Data_Bottles.png')

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

threshold = cv2.adaptiveThreshold(grayBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)

edges = cv2.Canny(grayBlur,10,75)

kernel = np.ones((3,3), np.uint8)
dilation = cv2.dilate(edges, kernel, iterations=5)

kernel = np.ones((3,3), np.uint8)
closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations=5)

kernel = np.ones((5,5), np.uint8)
opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations=3)

result_img = opening.copy()
contours, hierarchy = cv2.findContours(result_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# วาดวงกลมรอบๆ ขวด
counter = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area>300 and area < 2500:
        if len(cnt) >= 5:   
            ellipse = cv2.fitEllipse(cnt)
            cv2.ellipse(img, ellipse, (0,255,0), 2)
            counter += 1

cv2.putText(img, str(counter), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 2, cv2.LINE_AA)
cv2.imshow('Ops', edges)
cv2.imshow('Bottles', img)
print("Number of bottles detected:", counter)

k = cv2.waitKey(0)
cv2.destroyAllWindows()