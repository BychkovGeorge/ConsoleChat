import socket
import threading
import time
import queue

# Буфер
buffer_synchronizing = queue.Queue()
buffer_covert_sending = queue.Queue()
is_synchronizing = queue.Queue()
is_covert_sending = queue.Queue()


# Имитация сетевого экрана
def listener():
    while True:
        data, address = sor.recvfrom(1024)
        if address[1] == 5001:
            if is_synchronizing.empty() and is_covert_sending.empty():
                sor.sendto(data, SECOND_CLIENT_ADDRESS)
            elif not is_synchronizing.empty():
                buffer_synchronizing.put_nowait(data)
            elif not is_covert_sending.empty():
                buffer_covert_sending.put_nowait(data)
        if address[1] == 5002:
            sor.sendto(data, FIRST_CLIENT_ADDRESS)


def synchronizer():
    counter = 0
    while True:
        if buffer_synchronizing.empty():
            sor.sendto(''.encode('utf-8'), SECOND_CLIENT_ADDRESS)
            counter += 1
            time.sleep(1)
        else:
            sor.sendto(buffer_synchronizing.get_nowait(), SECOND_CLIENT_ADDRESS)
            counter += 1
            time.sleep(1)
        if counter == 5:
            break


def coverts_sender(covert_message):
    is_synchronizing.put_nowait(1)
    synchronizer()
    useless = is_synchronizing.get_nowait()
    is_covert_sending.put_nowait(1)
    lst = list(covert_message)
    for index in range(len(lst)):
        if lst[index] == '1':
            if buffer_covert_sending.empty():
                sor.sendto(''.encode('utf-8'), SECOND_CLIENT_ADDRESS)
                time.sleep(1)
            else:
                sor.sendto(buffer_covert_sending.get_nowait(), SECOND_CLIENT_ADDRESS)
                time.sleep(1)
        if lst[index] == '0':
            time.sleep(1)
    while not buffer_synchronizing.empty():
        sor.sendto(buffer_synchronizing.get_nowait(), SECOND_CLIENT_ADDRESS)
    while not buffer_covert_sending.empty():
        sor.sendto(buffer_covert_sending.get_nowait(), SECOND_CLIENT_ADDRESS)
    more_useless = is_covert_sending.get_nowait()


# Параметры сокета
FIRST_CLIENT_ADDRESS = ('127.0.0.1', 5001)
SECOND_CLIENT_ADDRESS = ('127.0.0.1', 5002)
MY_ADDRESS = ('127.0.0.1', 5010)
sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sor.bind(MY_ADDRESS)

thread = threading.Thread(target=listener)
thread.start()

# Закладка
print('Введите строку из 5 нулей и единиц')
msg = ''
while True:
    secret_message = input()
    list_of_symbols = list(secret_message)
    if len(list_of_symbols) != 5:
        print('Введено неправильное количество символов')
        continue
    error_counter = 0
    for i in range(len(list_of_symbols)):
        if list_of_symbols[i] != '0' and list_of_symbols[i] != '1':
            error_counter += 1
            break
    if error_counter == 0:
        print('Введённая последовательность принята, начинаю передачу...')
        msg = secret_message
        break
    else:
        print('Введённая строка состоит не только из "0" и "1"')
        continue

coverts_sender(msg)
