# CppUMockify example

In order to show __cppumocify__ in action this small example project was created.
Using `cmake` cppumockify will generate the mock for `MyModule` in order to
test the `Greetings` module. 

The script to generate the mock is called `generate_mymodule_mock.sh` and it will
generate the `MyModule` mock in the `example/bld/tst` folder.

## Installing dependencies for example

Make sure you have `cmake` installed and installed `cppumockify`

## Building example

In the `example` folder let create a build folder and let cmake generate the makefiles:

    mkdir -p bld
    cd bld
    cmake ..

Then build the example using:

    make

After building it the test in `example/bld` can be run:

    bld/test_greeting

