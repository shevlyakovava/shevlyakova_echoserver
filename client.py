
import socket

host = input('Введите айпи: ').split('.')
for i in range(len(host)):  
    while True:

        if (not host[i].isdigit()) and (int(host[i]) > 255 or int(host[i]) < 0 or len(host) != 4): 
            print(host, 'введено некорректно, введите заново!')
            host = input('Введите айпи: ').split('.')
            continue
        else:
            break
main_ip = ''
for r in range(len(host)):
    main_ip += str(host[r]) + '.'
main_ip = main_ip[:-1]

HOST = main_ip

while True:
    new_port = input('Введите номер порта, если хотите поставить значение по умолчанию (65432) введите 1: ') 
    if new_port.isdigit():
        if int(new_port) == 1:
            PORT = 65432  
            break
        elif int(new_port) > 65535 or int(new_port) < 1025: 
            print('Введены неверные значения!')
            continue
        else:
            PORT = int(new_port)
            break
    else:
        print('Введены неверные значения!')
        continue



while True:
    command = input('[CLIENT]: ')
    if command == 'do': 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
            s.connect((HOST, PORT)) 
            s.sendall(b'Hello, world') 
            data = s.recv(1024)  
            print(data.decode('UTF-8')) 
        continue
    elif command == 'exit':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b'exit')
            data = s.recv(1024)
            print(data.decode('UTF-8'))
        break
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(command.encode())
            data = s.recv(1024)
            print(data.decode('UTF-8'))
        continue

