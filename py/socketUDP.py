#!/usr/bin/python
import socket

server_ip = 'IP'  # IP do servidor
server_port = 53  # Porta do servidor

message = 'Olá, servidor!'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client_socket.sendto(message.encode(), (server_ip, server_port))

    data, server_address = client_socket.recvfrom(1024)
    print('Resposta do servidor:', data.decode())
    
except Exception as e:
    print('Erro:', e)

finally:
    client_socket.close()
