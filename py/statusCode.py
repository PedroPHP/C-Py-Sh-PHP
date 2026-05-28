#!/usr/bin/python
import requests

site = request.get("Seu site aqui")
status = site.status_code

if (status == 200):
	print ("Pagina existe")
else:
	print ("Pagina Inesxistente")
