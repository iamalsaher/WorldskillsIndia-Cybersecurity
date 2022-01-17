#include <stdio.h>

int buff[512];
int main(int argc, char **argv){
	fgets(buff, 512, stdin);
	printf(buff);
	return 0;
}