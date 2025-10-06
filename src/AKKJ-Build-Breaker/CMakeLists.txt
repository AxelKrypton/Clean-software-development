cmake_minimum_required(VERSION 3.26.0)

project(SU2)

include_directories(external)

add_executable(pow pow.cpp su2.cpp)
enable_testing()
add_subdirectory(tests)