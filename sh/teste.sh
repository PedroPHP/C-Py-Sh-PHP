#!/bin/bash

# Verifica se o usuário forneceu os argumentos corretamente
if [ $# -ne 2 ]; then
    echo "Uso: $0 <domínio> <arquivo_de_lista>"
    exit 1
fi

domain=$1
lista=$2

# Verifica a disponibilidade do domínio
echo "Verificando disponibilidade de $domain..."
ping -c 1 $domain > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "$domain não está acessível."
    exit 1
fi

# Descobre o IP do domínio
ip=$(dig +short $domain)
echo "IP do domínio $domain: $ip"

# Verifica cabeçalhos HTTP do domínio principal
echo "Cabeçalhos HTTP de $domain:"
http_status=$(curl -s -o /dev/null -w "%{http_code}" $domain)
if [ $http_status -eq 200 ]; then
    echo "$domain está ativo."
fi

# Lê a lista de subdomínios do arquivo fornecido
echo "Descobrindo subdomínios de $domain a partir de $lista..."
subdomains=$(cat $lista)

# Loop sobre cada subdomínio encontrado
for subdomain in $subdomains; do
    ip=$(dig +short $subdomain.$domain)
    if [ -n "$ip" ]; then
        http_status=$(curl -s -o /dev/null -w "%{http_code}" $subdomain.$domain)
        if [ $http_status -eq 200 ]; then
            echo "$subdomain.$domain está ativo."
        fi
    fi
done
