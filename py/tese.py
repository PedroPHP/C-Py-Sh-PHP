#!/usr/bin/python
import socket

# Endereço IP e porta do servidor UDP
server_ip = '37.59.174.227'  # IP do servidor
server_port = 53  # Porta do servidor

# Mensagem a ser enviada ao servidor
message = 'Olá, servidor!'

# Cria um socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Envia a mensagem para o servidor
    client_socket.sendto(message.encode(), (server_ip, server_port))

    # Aguarda a resposta do servidor
    data, server_address = client_socket.recvfrom(1024)
    print('Resposta do servidor:', data.decode())
    
except Exception as e:
    print('Erro:', e)

finally:
    # Fecha o socket
    client_socket.close()
