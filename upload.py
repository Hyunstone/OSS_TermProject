import cv2
from tkinter import *
from tkinter import filedialog
from os import path
import threading

def main():
    root = Tk()  #버튼 창을 만든다

    label = Label(root, text = '버튼을 선택하세요.') 
    label.pack()

    button = Button(root, text = '파일 열기', command = fileSearch)  #버튼 생성 및 버튼을 눌렀을 때 fileSearch함수 실행
    button.pack(side = LEFT, padx = 50,pady = 10) #side로 배치설정, padx로 좌우 여백설정, pady로 상하 여백설정 

    button2 = Button(root, text ='사진 촬영', command = photo)   #버튼 생성 및 버튼을 눌렀을 때 photo함수 실행
    button2.pack(side = LEFT, padx = 10, pady = 10)
    
    root.mainloop()  #root창을 띄운다
    
if __name__ == "__main__":
    main()