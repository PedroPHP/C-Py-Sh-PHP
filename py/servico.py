#!/usr/bin/python
import socket

print ("Interagindo com ftp server")
ip = input("digite o ip:")
porta = 21

meusocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
meusocket.connect_ex((ip,porta))
banner = meusocket.recv(1024)
print (banner)

print ("Enviando usuario")
meusocket.send(str.encode("USER ricardo\r \n"))
banner = meusocket.recv(1024)
print (banner)

print ("Enviando senha")
meusocket.send(str.encode("pass ricardo\r \n"))
banner = meusocket.recv(1024)
print (banner)
