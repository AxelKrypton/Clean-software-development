add_library(su2_lib STATIC su2.cpp)
target_include_directories(su2_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})