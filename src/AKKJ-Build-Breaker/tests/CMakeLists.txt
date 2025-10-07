add_executable(test_pow test_pow.cpp)
target_link_libraries(test_pow PRIVATE su2_lib)
add_test(NAME test_pow COMMAND test_pow)

add_executable(test_dummy test.cpp)
target_link_libraries(test_dummy PRIVATE su2_lib)
add_test(NAME test_dummy COMMAND test_dummy)