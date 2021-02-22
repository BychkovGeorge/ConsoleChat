import socket
import threading


def listener():
    while True:
        data = sor.recv(1024)
        msg = data.decode('utf-8')
        if msg != '':
            print(msg)


PROXY_ADDRESS = ('127.0.0.1', 5010)
MY_ADDRESS = ('127.0.0.1', 5001)
sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sor.bind(MY_ADDRESS)

thread = threading.Thread(target=listener)
thread.start()

while True:
    message = input()
    sor.sendto(message.encode('utf-8'), PROXY_ADDRESS)
