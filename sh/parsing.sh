#!/bin/bash
#https://github.com/desecsecurity/parsing_html_bash/blob/master/parsing_html.sh
if [ "$1" = "" ];
then
echo "Parsing HTML"
echo "Modo de uso: $0 site"
else
wget -b $1 -O FILE
echo "====================================================="
echo "[+] Resolvendo URLs em: $1"
grep href FILE
#grep href index.html | cut -d "/" -f 3 | grep \. | cut -d '"' -f 1 | grep -v "<" | grep -v ">"

echo "====================================================="
echo "[+] Concluido: Salvando os resultados em: $1.txt"
#for url in $(cat $1.txt);
#do
#host $url;
#done
echo "====================================================="
fi
