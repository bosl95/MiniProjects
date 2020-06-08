import socket
import time

s = socket.socket()
s.bind(('192.168.137.1', 7070))
s.listen(True)

while True:
    c, addr = s.accept()
    print('connection')
    size = int(c.recv(1024).decode('utf-8'))
    print(size)
    filename = c.recv(1024).decode('utf-8')   # 이미지의 크기를 미리 받아옴
    print(filename)
    time.sleep(1)

    with open(filename, 'wb') as f:
        buf = b''
        while size:
            newbuf = c.recv(size)
            if not newbuf: break
            buf += newbuf
            size -= len(newbuf)
        f.write(buf)
    print('저장 완료')