#include <stdio.h>

#include "MyModule.h"

void MyModule_SayHello(const char name[])
{
    printf("Hello %s\n", name);
}

void MyModule_SayGoodbye(void)
{
    printf("Goodbye\n");
}
