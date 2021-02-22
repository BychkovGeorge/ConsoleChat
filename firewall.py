import socket
import threading
import time


# Имитация сетевого экрана
def listener():
    while True:
        data, address = sor.recvfrom(1024)
        if address[1] == 5001:
            sor.sendto(data, SECOND_CLIENT_ADDRESS)
        if address[1] == 5002:
            sor.sendto(data, FIRST_CLIENT_ADDRESS)


def synchronizer():
    counter = 0
    while True:
        sor.sendto(''.encode('utf-8'), SECOND_CLIENT_ADDRESS)
        counter += 1
        time.sleep(1)
        if counter == 5:
            break


def coverts_sender(covert_message):
    synchronizer()
    lst = list(covert_message)
    for index in range(len(lst)):
        if lst[index] == '1':
            sor.sendto(''.encode('utf-8'), SECOND_CLIENT_ADDRESS)
            time.sleep(1)
        if lst[index] == '0':
            time.sleep(1)


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
