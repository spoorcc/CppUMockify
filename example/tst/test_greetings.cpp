#include "CppUTest/CommandLineTestRunner.h"
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"

#include <Greetings.h>

int main(int ac, char** av)
{
    return CommandLineTestRunner::RunAllTests(ac, av);
}

TEST_GROUP(GreetingsTest)
{
    void teardown()
    {
        mock().clear();
    }
};

TEST(GreetingsTest, IsGoodbyeSaid)
{
    /* Setup */
    mock().expectOneCall("MyModule_SayHello").withParameter("name", "Marco");
    mock().expectOneCall("MyModule_SayGoodbye");

    /* Exercise */
    Greetings_DoStuff("Marco");

    /* Verify */
    mock().checkExpectations();
}
