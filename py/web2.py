#!/usr/bin/python
form urllib.request import urlopen

site = uurlopen("http://businescorp.com.br")
server = site.info()

print ("O servidor web esta rodando")
print (server ["Server"])
