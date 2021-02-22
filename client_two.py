import socket
import threading
import time


def listener():
    timestamps = []
    timestamps_differences = []
    while True:
        data = sor.recv(1024)
        msg = data.decode('utf-8')
        if len(timestamps) == 0:
            timestamps.append(time.time())
        else:
            time_now = time.time()
            index = len(timestamps)
            if time_now - timestamps[index - 1] < 1.1:
                timestamps.append(time_now)
                timestamps_differences.append(time_now - timestamps[index - 1])
            else:
                timestamps = []
                timestamps_differences = []
        print(len(timestamps))
        if msg != '':
            print(msg)


PROXY_ADDRESS = ('127.0.0.1', 5010)
MY_ADDRESS = ('127.0.0.1', 5002)
sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sor.bind(MY_ADDRESS)

thread = threading.Thread(target=listener)
thread.start()

while True:
    message = input()
    sor.sendto(message.encode('utf-8'), PROXY_ADDRESS)
