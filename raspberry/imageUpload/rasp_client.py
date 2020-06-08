import tkinter as tk
import os
from tkinter import *
from tkinter import messagebox as msg
import picamera
import time
from PIL import Image, ImageTk
import io
import socket
import time


def photoSize():
    image = Image.open(folderEntry.get() + '/' + fileEntry.get() + '.png')
    image = image.resize((600, 300), Image.ANTIALIAS)
    return image    # captureBoard에 출력하기 위해 resize한 사진 크기를 반환


def captureClick(): # 촬영 버튼을 클릭하면 발생하는 이벤트
    rv = radioValue.get()
    if rv == 0: # 라디오 버튼 클릭이 안되있는 경우 아무것도 실행하지 않고 종료함.
        msg.showinfo('촬영 실패', '적용할 효과를 선택해주세요')
        return

    if not os.path.isdir(os.getcwd() + '/' + folderEntry.get()):  # 폴더가 없는 경우 생성해준다.
        os.mkdir(folderEntry.get())
        msg.showinfo('폴더가 존재하지 않습니다. ', folderEntry.get() + ' 폴더가 자동 생성되었습니다.')

    if os.path.isfile(os.getcwd() + '/' + folderEntry.get() + '/' + fileEntry.get() + '.png'):   # 파일이 이미 존재하는 경우 함수 종료
        msg.showinfo('실패', '중복된 파일명을 사용할 수 없습니다.')
        return
    else:
        c.image_effect = mode[rv - 1] # 사진 촬영 모드 설정
        c.capture(folderEntry.get() + '/' + fileEntry.get() + '.png')  # 사진을 찍어서 해당 폴더에 저장
    print('사진 저장 완료')

    img = ImageTk.PhotoImage(photoSize())
    lbl = tk.Label(root, image=img)
    lbl.image = img
    lbl.grid(row=1, column=4)
    label3.configure(text=fileEntry.get() + '.png') # 이미지를 captureboard에 띄움


def uploadClick():   # upload 버튼을 클릭하면 실행되는 함수
    if label3['text'] == 'image name':  # captureboard에 올라온 사진이 없는 경우 (사진이 촬영되지 않은 경우) 업로드할 사진이 없으므로 함수를 종료
        msg.showinfo('error', '업로드할 사진이 없습니다.')
        return
    print('upload')
    s = socket.socket()
    s.connect(('192.168.137.1', 7070))  # 서버와 연결
    print('connecting...')

    # 파일 크기 전송
    s.sendall(str(os.path.getsize(folderEntry.get() + '/' + fileEntry.get() + '.png')).encode('utf-8'))

    # 파일 이름을 반환
    s.sendall((fileEntry.get() + '.png').encode('utf-8'))

    time.sleep(1)   # 버퍼를 위해서 2초 대기

    data = open(folderEntry.get() + '/' + fileEntry.get() + '.png', 'rb')
    s.sendall(data.read())

    s.close()   # 소켓 닫기
    msg.showinfo('성공', '파일이 전송되었습니다.')


root = tk.Tk()
root.title('camera')
root.geometry("950x600+50+50")

radioValue = tk.IntVar()
c = picamera.PiCamera()
mode = ['pastel', 'negative', 'cartoon']

label = tk.Label(root, text='폴더명')
label2 = tk.Label(root, text='파일명')
folderEntry = tk.Entry(root)
folderEntry.insert(0, 'PRimage')    # entry의 text 값을 미리 생성 ( 빠른 입력을 위한 설정)
fileEntry = tk.Entry(root)
fileEntry.insert(0, 'capture')   # entry의 text 값을 미리 생성 ( 빠른 입력을 위한 설정)
captureButton = tk.Button(root, text='촬영', width=15, command=captureClick)
captureBoard = tk.Canvas(root, width=100, height=100)
radioLabel = tk.Label(root, text='효과')

radio1 = tk.Radiobutton(root, text=mode[0], variable=radioValue, value=1)
radio2 = tk.Radiobutton(root, text=mode[1], variable=radioValue, value=2)
radio3 = tk.Radiobutton(root, text=mode[2], variable=radioValue, value=3)
label3 = tk.Label(root, text='image name')
uploadButton = tk.Button(root, text='upload', command=uploadClick)

label.grid(row=0, column=0)
folderEntry.grid(row=0, column=1)
label2.grid(row=1, column=0)
fileEntry.grid(row=1, column=1)
captureButton.grid(row=2, column=0, columnspan=2, sticky=W + E + N + S)
captureBoard.grid(row=0, column=4, sticky=W + E + N + S)
radioLabel.grid(row=4, column=1)
radio1.grid(row=5, column=0, columnspan=1, sticky=W + E + N + S)
radio2.grid(row=5, column=1, columnspan=1, sticky=W + E + N + S)
radio3.grid(row=5, column=2, columnspan=1, sticky=W + E + N + S)

label3.grid(row=5, column=3, columnspan=3, sticky=W + E + N + S)
uploadButton.grid(row=6, column=3, columnspan=3, sticky=W + E + N + S)

root.mainloop()
