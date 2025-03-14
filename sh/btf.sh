#!/bin/bash

# Função para realizar a busca em subdiretórios
buscar_subdiretorios() {
    local domain="$1"
    local subdir="$2"
    local wordlist="$3"

    # Loop sobre cada nome de arquivo na lista
    while IFS= read -r filename; do
        # Monta a URL completa para o arquivo
        url="http://$domain/$subdir/$filename"
        
        # Faz uma requisição HTTP HEAD para verificar se o arquivo existe
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        
        # Verifica se a resposta é 200 (OK)
        if [[ "$response" == 200  || "$response" == 301]]; then
            echo "Arquivo encontrado: $url"
            # Você pode adicionar aqui qualquer lógica para processar o arquivo encontrado,
            # como baixá-lo ou extrair informações dele.
        fi
    done < "$wordlist"
}

# Função principal para buscar diretórios e subdiretórios
buscar_diretorios() {
    local domain="$1"
    local wordlist="$2"

    # Loop sobre cada nome de diretório na lista
    while IFS= read -r directory; do
        # Monta a URL completa para o diretório
        url="http://$domain/$directory/"
        
        # Faz uma requisição HTTP HEAD para verificar se o diretório existe
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        
        # Verifica se a resposta é 200 (OK)
        if [[ "$response" == 200  ||  "$response" == 301]]; then
            echo "Diretório encontrado: $url"
            # Chama a função para buscar subdiretórios
            buscar_subdiretorios "$domain" "$directory" "$wordlist"
        fi
    done < "$wordlist"
}

# Verifica se o usuário forneceu os argumentos corretamente
if [ $# -lt 2 ]; then
    echo "Uso: $0 <domínio> <arquivo_de_lista>"
    exit 1
fi

domain="$1"
wordlist="$2"

# Chama a função principal para iniciar a busca de diretórios
buscar_diretorios "$domain" "$wordlist"
