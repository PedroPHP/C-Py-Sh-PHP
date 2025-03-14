#!/bin/bash

# Verifica se o usuário forneceu os argumentos corretamente
if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    echo "Uso: $0 <domínio> <arquivo_de_lista> [extensão]"
    exit 1
fi

domain=$1
lista=$2
extension=$3

# Função para verificar os subdomínios com uma determinada extensão
verificar_subdominios_com_extensao() {
    local ext="$1"
    echo "Descobrindo subdomínios de $domain a partir de $lista com a extensão .$ext..."
    
    # Inicializa arrays para cada tipo de status
    declare -A status_200
    declare -A status_301

    # Loop sobre cada subdomínio encontrado com a extensão especificada
    while IFS= read -r subdomain; do
        subdomain=$(basename "$subdomain")  # Remove o caminho completo
        echo "Verificando com a extensão .$ext: $domain/$subdomain"
        http_status=$(curl -s -o /dev/null -w "%{http_code}" "$domain/$subdomain.$ext")
        if [ $http_status -eq 200 ]; then
            status_200["$domain/$subdomain.$ext"]="Status: $http_status"
            resolver_dns "$domain/$subdomain.$ext"
        elif [ $http_status -eq 301 ]; then
            status_301["$domain/$subdomain.$ext"]="Status: $http_status"
            resolver_dns "$domain/$subdomain.$ext"
        fi
    done < "$lista"

    # Exibe os resultados agrupados por status e extensão
    echo "Resultados para a extensão .$ext:"
    echo "Status 200:"
    for result in "${!status_200[@]}"; do
        echo "$result, ${status_200[$result]}, IP: ${ips[$result]}"
    done

    echo "Status 301:"
    for result in "${!status_301[@]}"; do
        echo "$result, ${status_301[$result]}, IP: ${ips[$result]}"
    done
}

# Função para verificar os subdomínios sem extensão
verificar_subdominios_sem_extensao() {
    echo "Descobrindo subdomínios de $domain a partir de $lista sem extensão..."
    
    # Inicializa arrays para cada tipo de status
    declare -A status_200
    declare -A status_301

    # Loop sobre cada subdomínio encontrado sem extensão
    while IFS= read -r subdomain; do
        subdomain=$(basename "$subdomain")  # Remove o caminho completo
        echo "Verificando sem extensão: $domain/$subdomain"
        http_status=$(curl -s -o /dev/null -w "%{http_code}" "$subdomain.$domain")
        if [ $http_status -eq 200 ]; then
            status_200["$domain/$subdomain"]="Status: $http_status"
            resolver_dns "$domain/$subdomain"
        elif [ $http_status -eq 301 ]; then
            status_301["$domain/$subdomain"]="Status: $http_status"
            resolver_dns "$domain/$subdomain"
        fi
    done < "$lista"

    # Exibe os resultados agrupados por status para subdomínios sem extensão
    echo "Resultados sem extensão:"
    echo "Status 200:"
    for result in "${!status_200[@]}"; do
        echo "$result, ${status_200[$result]}, IP: ${ips[$result]}"
    done

    echo "Status 301:"
    for result in "${!status_301[@]}"; do
        echo "$result, ${status_301[$result]}, IP: ${ips[$result]}"
    done
}

# Função para resolver o DNS e obter os IPs
resolver_dns() {
    local domain="$1"
    local ip=$(dig +short "$domain")
    if [ -n "$ip" ]; then
        ips["$domain"]=$ip
    else
        ips["$domain"]="Não foi possível resolver o IP"
    fi
}

# Verifica a disponibilidade do domínio principal
echo "Verificando disponibilidade de $domain..."
ping -c 1 "$domain" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "$domain não está acessível."
    exit 1
fi

# Descobre o IP do domínio principal
ip=$(dig +short "$domain")
echo "IP do domínio $domain: $ip"

# Verifica cabeçalhos HTTP do domínio principal
echo "Cabeçalhos HTTP de $domain:"
http_status=$(curl -s -o /dev/null -w "%{http_code}" "$domain")
if [ $http_status -eq 200 ] || [ $http_status -eq 301 ] || [ $http_status -eq 500 ]; then
    echo "$domain está ativo, Status: $http_status"
fi

# Se o usuário especificou uma extensão, verificar os subdomínios com essa extensão
if [ -n "$extension" ]; then
    verificar_subdominios_com_extensao "$extension"
fi

# Verificar os subdomínios sem a extensão especificada
verificar_subdominios_sem_extensao
