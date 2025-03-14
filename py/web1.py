#!/usr/bin/python
import requests

site = request.get("http://businescorp.com.br")
status = site.status_code

if (status == 200):
	print ("Pagina existe")
else:
	print ("Pagina Inesxistente")
