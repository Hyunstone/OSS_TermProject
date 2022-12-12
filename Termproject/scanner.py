import sys
import numpy as np
import cv2
import imutils
from tkinter import *
from tkinter import filedialog
from os import path
import threading
from file_choice import fileSearch, snapshot, catptureButtonRun, playCam, Photo


a = 0
choiceFileSrc = 0
def fileSearch():
    global choiceFileSrc
    file = filedialog.askopenfilename(initialdir= path.dirname(__file__))
    choiceFileSrc = file

def drawROI(choiceFileSrc, corners):
    cpy = choiceFileSrc.copy()

    c1 = (192, 192, 255)
    c2 = (128, 128, 255)

    for pt in corners:
        cv2.circle(cpy, tuple(pt.astype(int)), 25, c1, -1, cv2.LINE_AA)

    cv2.line(cpy, tuple(corners[0].astype(int)), tuple(corners[1].astype(int)), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[1].astype(int)), tuple(corners[2].astype(int)), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[2].astype(int)), tuple(corners[3].astype(int)), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[3].astype(int)), tuple(corners[0].astype(int)), c2, 2, cv2.LINE_AA)

    disp = cv2.addWeighted(choiceFileSrc, 0.3, cpy, 0.7, 0)

    return disp

def onMouse(event, x, y, flags, param):
    global srcQuad, dragSrc, ptOld, src

    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(4):
            if cv2.norm(srcQuad[i] - (x, y)) < 25:
                dragSrc[i] = True
                ptOld = (x, y)
                break

    if event == cv2.EVENT_LBUTTONUP:
        for i in range(4):
            dragSrc[i] = False

    if event == cv2.EVENT_MOUSEMOVE:
        for i in range(4):
            if dragSrc[i]:
                dx = x - ptOld[0]
                dy = y - ptOld[1]

                srcQuad[i] += (dx, dy)

                cpy = drawROI(src, srcQuad)
                cv2.imshow('img', cpy)
                ptOld = (x, y)
                break
    

def main():
    root = Tk()

    label = Label(root, text = '명령을 실행하고 종료하세요') 
    label.pack()

    button = Button(root, text = '파일 열기', command = fileSearch)
    button.pack(side = LEFT, padx = 50,pady = 10) #side로 배치설정, padx로 좌우 여백설정, pady로 상하 여백설정 

    button2 = Button(root, text ='사진 촬영', command = Photo)
    button2.pack(side = LEFT, padx = 10, pady = 10)
    
    
    root.mainloop()
    
if __name__ == "__main__":
    main()



# 입력 이미지 불러오기
src = cv2.imread(choiceFileSrc)
src = imutils.resize(src, height = 800)

if src is None:
    print('Image open failed!')
    sys.exit()

# 입력 영상 크기 및 출력 영상 크기
h, w = src.shape[:2]
dw = 500
dh = round(dw * 297 / 210)  # A4 용지 크기: 210x297cm

# 모서리 점들의 좌표, 드래그 상태 여부
srcQuad = np.array([[30, 30], [30, h-30], [w-30, h-30], [w-30, 30]], np.float32)
dstQuad = np.array([[0, 0], [0, dh-1], [dw-1, dh-1], [dw-1, 0]], np.float32)
dragSrc = [False, False, False, False]

# 모서리점, 사각형 그리기
disp = drawROI(src, srcQuad)

cv2.imshow('img', disp)
cv2.setMouseCallback('img', onMouse)

while True:
    key = cv2.waitKey()
    if key == 13:  # ENTER 키
        break
    elif key == 27:  # ESC 키
        cv2.destroyWindow('img')
        sys.exit()

# 투시 변환
pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
dst = cv2.warpPerspective(src, pers, (dw, dh), flags=cv2.INTER_CUBIC)

# 결과 영상 출력
cv2.imshow('Scan', dst)
cv2.imwrite(choiceFileSrc, dst)
cv2.waitKey()
cv2.destroyAllWindows()


imgPath = choiceFileSrc
img = cv2.imread(imgPath)
orig = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edge = cv2.Canny(blur, 75, 200)

th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
# th__ = cv2.adaptiveThreshold(edge,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv2.THRESH_BINARY,11,2)

cv2.imshow("Transform", th)
# cv2.imshow("edge", th__)
cv2.imwrite("Transformed scan image.jpg", th)
cv2.waitKey(0)
cv2.destroyAllWindows()	
