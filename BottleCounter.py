import cv2
import numpy as np
img = cv2.imread('./Data_Bottles.png')
height, width, _ = img.shape
img = img[5:height-30, 130:width-10]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur เพื่อลด noise และทำให้ขอบของขวดชัดเจนขึ้น
# grayBlur = cv2.GaussianBlur(gray, (15,15), 0)
grayBlur = cv2.medianBlur(gray, 15, 0)


threshold = cv2.adaptiveThreshold(grayBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)


### ลองใช้ Morphology operations
kernel = np.ones((2,2), np.uint8)
opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=3)

kernel = np.ones((5,5), np.uint8)
erosion = cv2.erode(opening, kernel, iterations=1)

kernel = np.ones((3,3), np.uint8)
dilation = cv2.dilate(erosion, kernel, iterations=3)

kernel = np.ones((5,5), np.uint8)
erosion = cv2.erode(dilation, kernel, iterations=1)
# kernel = np.ones((3,3), np.uint8)
# opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel, iterations=3)
kernel = np.ones((3,3), np.uint8)
closing = cv2.morphologyEx(erosion, cv2.MORPH_CLOSE, kernel, iterations=3)

kernel = np.ones((5,5), np.uint8)
dilation = cv2.dilate(closing, kernel, iterations=3)
### ลองใช้ Morphology operations


result_img = dilation.copy()
contours, hierarchy = cv2.findContours(result_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# วาดวงกลมรอบๆ ขวด
counter = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area>500 and area < 5000:        
        ellipse = cv2.fitEllipse(cnt)
        cv2.ellipse(img, ellipse, (0,255,0), 2)
        counter += 1

cv2.putText(img, str(counter), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 2, cv2.LINE_AA)
cv2.imshow('Bottles', dilation)

k = cv2.waitKey(0)
cv2.destroyAllWindows()