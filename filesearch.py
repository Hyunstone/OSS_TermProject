import cv2
from tkinter import *
from tkinter import filedialog
from os import path
import threading

#파일 탐색기를 통해 파일을 찾는 함수
def fileSearch():
    file = filedialog.askopenfilename(initialdir= path.dirname(__file__))
    print(file)