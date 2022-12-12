import cv2
from tkinter import *
from tkinter import filedialog
from os import path
import threading

a = 0

# 함수 정의 (버튼을 누르면 텍스트 내용이 바뀜)
def fileSearch():
    file = filedialog.askopenfilename(initialdir= path.dirname(__file__))
    choiceFileSrc = file
    print(file)
    

def snapshot():
    global a
    a = 1

def catptureButtonRun():
    captureWindow = Toplevel()
    captureButton = Button(captureWindow, text = '촬영', command = snapshot)
    captureButton.pack(side = LEFT, padx = 100, pady = 50)
    
def playCam():
    # 사진 찍기
    camera = cv2.VideoCapture(0) # 카메라 open
    
    if not camera.isOpened():
        print("Camera open failed!")
        exit()
    else:
        while True:
            ret, frame = camera.read() # 영상 읽기. ret: 처리결과(bool), frame: 읽어온 영상(1프레임)
            if not ret:
                print("Can't read camera")
                break
            else:
                cv2.imshow('PC_camera', frame)
                # 사진 촬영에서 스페이스키를 입력하면 촬영 완료
                if cv2.waitKey(32) == 32:
                    cv2.imwrite('photo.jpg', frame)
                    break
                # 사진 촬영에서 촬영버튼 클릭하면 촬영 완료
                if a == 1:
                    cv2.imwrite('photo.jpg', frame)
                    break
                
    camera.release()
    cv2.destroyAllWindows()
    
def Photo():
    captureButtonThread = threading.Thread(target = catptureButtonRun)
    captureButtonThread.daemon = True
    captureButtonThread.start()
    
    photo_thread = threading.Thread(target = playCam)
    photo_thread.daemon = True
    photo_thread.start()
    
def main():
    root = Tk()

    label = Label(root, text = '버튼을 선택하세요.') 
    label.pack()

    button = Button(root, text = '파일 열기', command = fileSearch)
    button.pack(side = LEFT, padx = 50,pady = 10) #side로 배치설정, padx로 좌우 여백설정, pady로 상하 여백설정 

    button2 = Button(root, text ='사진 촬영', command = Photo)
    button2.pack(side = LEFT, padx = 10, pady = 10)
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
