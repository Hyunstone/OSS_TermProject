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