import socket
import threading
import time


def listener():
    timestamps = []
    timestamps_differences = []
    t = 0
    covert_message = ['0', '0', '0', '0', '0']
    while True:
        data = sor.recv(1024)
        msg = data.decode('utf-8')
        if len(timestamps) < 4:
            if len(timestamps) == 0:
                timestamps.append(time.time())
            else:
                time_now = time.time()
                index = len(timestamps)
                if 1.1 > time_now - timestamps[index - 1] > 0.9:
                    timestamps.append(time_now)
                    timestamps_differences.append(time_now - timestamps[index - 1])
                else:
                    timestamps = []
                    timestamps_differences = []
                    timestamps.append(time_now)
        elif len(timestamps) == 4:
            time_now = time.time()
            index = len(timestamps)
            if 1.1 > time_now - timestamps[index - 1] > 0.9:
                timestamps.append(time_now)
                timestamps_differences.append(time_now - timestamps[index - 1])
                t = time.time()
            else:
                timestamps = []
                timestamps_differences = []
                timestamps.append(time_now)
        elif len(timestamps) == 5:
            if 1.1 > time.time() - t > 0.9:
                covert_message[0] = '1'
            elif 2.1 > time.time() - t > 1.9:
                covert_message[1] = '1'
            elif 3.1 > time.time() - t > 2.9:
                covert_message[2] = '1'
            elif 4.1 > time.time() - t > 3.9:
                covert_message[3] = '1'
            elif 5.1 > time.time() - t > 4.9:
                covert_message[4] = '1'
            elif time.time() - t > 5.1:
                print(covert_message)
                timestamps = []
                timestamps_differences = []
                for i in range(len(covert_message)):
                    covert_message[i] = '0'
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
