
#include <MyModule.h>
#include <Greetings.h>


int Greetings_DoStuff(const char name[])
{
    MyModule_SayHello(name);
    MyModule_SayGoodbye();
}
