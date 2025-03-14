#!/bin/bash

# Verifica se o usuário forneceu os argumentos corretamente
if [ $# -ne 2 ]; then
    echo "------------------------------------"
    echo "-------------Web Recon--------------"
    echo "Uso: $0 <domínio> <arquivo_de_lista>"
    echo "------------------------------------"
    exit 1
fi

domain=$1
lista=$2

# Verifica a disponibilidade do domínio principal
echo "Verificando disponibilidade de $domain..."
echo "-----------------------------------------"
ping -c 1 $domain > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "$domain não está acessível."
    exit 1
fi

# Descobre o IP do domínio principal
ip=$(dig +short $domain)
echo "IP do domínio $domain: $ip"
echo "--------------------------"

# Verifica cabeçalhos HTTP do domínio principal
echo "Cabeçalhos HTTP de $domain:"
http_status=$(curl -s -o /dev/null -w "%{http_code}" $domain)
if [ $http_status -eq 200 ] || [ $http_status -eq 301 ] || [ $http_status -eq 500 ]; then
    echo "$domain está ativo, Status: $http_status"
    echo "----------------------------------------"
fi

# Lê a lista de subdomínios do arquivo fornecido
echo "Descobrindo subdomínios de $domain a partir de $lista..."
echo "--------------------------------------------------------"
subdomains=$(cat $lista)

# Inicializa arrays para cada tipo de status
status_200=()
status_301=()
status_404=()
status_other=()

# Loop sobre cada subdomínio encontrado
for subdomain in $subdomains; do
    http_status=$(curl -s -o /dev/null -w "%{http_code}" $domain/$subdomain)
    if [ $http_status -eq 200 ]; then
        status_200+=("$domain/$subdomain, Status: $http_status")
    elif [ $http_status -eq 301 ]; then
        status_301+=("$domain/$subdomain, Status: $http_status")
    elif [ $http_status -eq 404 ]; then
        status_404+=("$domain/$subdomain, Status: $http_status")
    else
        status_other+=("$domain/$subdomain, Status: $http_status")
    fi
done

# Exibe os resultados agrupados por status
echo "Resultados:"
echo "Status 200:"
for result in "${status_200[@]}"; do
    echo "$result"

done

echo "Status 301:"
for result in "${status_301[@]}"; do
    echo "$result"

done

echo "Status 404:"
for result in "${status_404[@]}"; do
    echo "$result"

done

echo "Outros Status:"
for result in "${status_other[@]}"; do
    echo "$result"

done
