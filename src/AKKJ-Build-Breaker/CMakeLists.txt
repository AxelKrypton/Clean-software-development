cmake_minimum_required(VERSION 3.26.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(SU2)

include_directories(external)
add_subdirectory(src)

# add_executable(pow test_pow.cpp su2.cpp)
enable_testing()
add_subdirectory(tests)