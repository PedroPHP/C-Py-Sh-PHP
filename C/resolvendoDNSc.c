#include <stdio.h>
#include <netdb.h>
#include <arpa/inet.h>

int main(int argc, char *argv[]){

	if (argc <= 1 ){
		printf("Modo de uso: ./resolver www.site.com.br \n");
		return 0;
	}else{
		struct hostent *alvo = gethostbyname(argv[1]);
		if (alvo == NULL){
			printf("ocorreu um erro:\n");
		}else{
			printf("IP: %S\n",inet_ntoa(*((struct in_addr *)alvo->h_addr)));
	}
}
}
