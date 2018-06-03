cmake_minimum_required (VERSION 2.6)
project (Example)

####################################
# Get CppUTest as external
set(CPPUTEST_DIR ${CMAKE_BINARY_DIR}/ext/cpputest)
set(CPPUTEST_SRC_DIR ${CPPUTEST_DIR}/src/CppUtest)
set(CPPUTEST_INC_DIR ${CPPUTEST_SRC_DIR}/include)
set(CPPUTEST_LIB_DIR ${CPPUTEST_SRC_DIR}/src/CppUTest)
set(CPPUTESTEXT_LIB_DIR ${CPPUTEST_SRC_DIR}/src/CppUTestExt)

file(MAKE_DIRECTORY ${CPPUTEST_DIR})
include(ExternalProject)
externalproject_add(CppUTest-project
    PREFIX                ${CPPUTEST_DIR}
    GIT_REPOSITORY        https://github.com/cpputest/cpputest.git
    GIT_TAG               "v3.8"
    SOURCE_DIR            ${CPPUTEST_SRC_DIR}
    BUILD_IN_SOURCE       1
    CMAKE_COMMAND         "cmake"
    CMAKE_ARGS            -DTESTS=OFF
    INSTALL_COMMAND       ""
 )

include_directories(${CPPUTEST_INC_DIR})
link_directories(${CPPUTEST_LIB_DIR} ${CPPUTESTEXT_LIB_DIR})

include_directories(inc)

# Create our main binary
add_library(Greetings lib/Greetings.c)
add_library(MyModule lib/MyModule.c)
add_executable(example main.c)
target_link_libraries(example Greetings MyModule)

# Create a test for Greetings module
message(STATUS "Generating mock")
execute_process(COMMAND ${CMAKE_SOURCE_DIR}/generate_mymodule_mock.sh ${CMAKE_BINARY_DIR}/tst)
add_executable(test_greetings tst/test_greetings.cpp tst/MyModule_mock.cpp)
target_link_libraries(test_greetings Greetings CppUTest CppUTestExt)
add_dependencies(test_greetings CppUTest-project)
