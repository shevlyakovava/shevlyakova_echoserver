import socket
import random
import json
from datetime import datetime


def log(text):  
    print(text)
    current_time = datetime.now().time()
    with open('log.txt', 'a', encoding='UTF-8') as file:
        file.write(f'[%d:%d:%d]: ' % (current_time.hour, current_time.minute, current_time.second) + text + '\n')


while True:
    new_port = input('Введите номер порта, если хотите поставить значение по умолчанию (65432) введите 1: ')
    if new_port.isdigit():
        if int(new_port) == 1:
            PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
            break
        elif int(new_port) > 65535 or int(new_port) < 1025:  
            log('Введены неверные значения!')
            continue
        else:
            PORT = int(new_port)
            break
    else:
        log('Введены неверные значения!')
        continue

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)

try:
    with open('db.json', 'r', encoding='utf-8') as f: 
        reg_user = json.load(f)
except:
    reg_user = {}
    with open(f'db.json', 'w', encoding='utf-8') as f:  
        json.dump(reg_user, f, ensure_ascii=False, indent=4)


log('Сервер включен')
while True:
    current_time = datetime.now().time() 
    connection = []
    new_port_new = random.randint(1025, 65535)  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.bind((HOST, PORT))  
        s.listen() 
        log('Прослушивание порта...')
        conn, addr = s.accept() 
        print(addr)
        now = (addr[0], new_port_new)
        for i in connection:
            if i == addr[1]:
                addr = now
        connection.append(addr[1]) 
        save_port = (addr[1])
        with conn:  # коннектим клиента
            log(f'Connected by {addr} in %d:%d:%d ' % (current_time.hour, current_time.minute, current_time.second))
            while True:
                data = conn.recv(1024) 
                if not data: 
                    break
                check = data.decode("utf-8") 
                if addr[0] not in reg_user: 
                    reg_user[addr[0]] = 1
                    conn.sendall(data + ' [СЕРВЕР]Введите свои данные в формате "reg:имя,пароль"'.encode())
                elif reg_user[addr[0]] != 1:
                    with open('db.json', 'r', encoding='utf-8') as f:
                        reg_user = json.load(f)  
                    conn.sendall(data + (' [СЕРВЕР]Здравствуйте, ' + reg_user[addr[0]]['name']).encode()) 
                else:
                    conn.sendall(data)
                log(f'Отправка данных клиенту - {data.decode("utf-8")}')
        if 'reg:' in check: # запись имени и пароля
            check = check.split(':')
            check = check[1].split(',')
            reg_user[addr[0]] = {'name': 0, 'pass': 0}
            reg_user[addr[0]]['name'] = check[0]
            reg_user[addr[0]]['pass'] = check[1]
            with open(f'db.json', 'w', encoding='utf-8') as f:
                json.dump(reg_user, f, ensure_ascii=False, indent=4)
            continue

