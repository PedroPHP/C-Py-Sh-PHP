#!/usr/bin/python
import socket,sys

ip = input("digite o ip:")
porta = int(input("digite a porta:"))

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
res = socket.connect_ex((ip,porta))

if (res == 0):
	print ("porta aberta")
else:
	print ("porta fechada")
