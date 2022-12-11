import cv2

imgPath = "Termp\\input.jpg"
img = cv2.imread(imgPath)
orig = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edge = cv2.Canny(blur, 75, 200)

th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
th__ = cv2.adaptiveThreshold(edge,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

cv2.imshow("not edge", th)
cv2.imshow("edge", th__)
cv2.imwrite("Termp\\output.jpg", th)
cv2.waitKey(0)
cv2.destroyAllWindows()	