#!/bin/bash
if [ "$1" == "" ]
then
echo "Desec security - portscan network"
echo "Modo de uso: $0 Rede"
echo "Exemplo: $0 192.168.0"
else
for ip in {1..254}
do
hping3 -S -p 80 -c 1 $1.$ip | grep "Flags=SA";
done
fi
