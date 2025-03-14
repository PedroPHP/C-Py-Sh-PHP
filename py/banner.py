#!/usr/bin/python
import socket,sys

ip = raw_input("digite o ip:")
porta = int(input("digite a porta:"))

meusocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
meusocket.connect_ex((ip,porta))
banner = meusocket.recv(1024)
print (banner)
