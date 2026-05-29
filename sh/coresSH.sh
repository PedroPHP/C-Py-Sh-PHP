#!/bin/bash

# Define as cores
red='\033[0;31m'
green='\033[0;32m'
reset='\033[0m'

# Frase a ser colorida
frase="Esta frase está colorida!"

# Imprime a frase colorida
echo -e "Frase em ${red}vermelho${reset} e ${green}verde${reset}: $frase"
