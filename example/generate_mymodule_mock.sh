#!/usr/bin/sh

# Generate in the directory argument

echo "Will generate in $1"
mkdir -p $1
pushd $1
rm MyModule_mock.cpp
cppumockify MyModule 'void MyModule_SayHello(const char* name);'
cppumockify MyModule 'void MyModule_SayGoodbye(void);'
popd
