#!/bin/bash
if [ "$1" == "" ]
then
echo "Desec security - portscan network"
echo "Modo de uso: $0 Rede porta"
echo "Exemplo: $0 192.168.0 80"
else
for ip in {1..254}
do
hping3 -S -p $2 -c 1 $1.$ip 2> /dev/nulld | grep "flags=SA" | cut -d " " -f 2 | cut -d "=" -f 2;
done
fi
