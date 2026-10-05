#include <stdlib.h>
int main(void){int*p=malloc(sizeof *p);if(!p)return 2;*p=7;free(p);return *p;}
