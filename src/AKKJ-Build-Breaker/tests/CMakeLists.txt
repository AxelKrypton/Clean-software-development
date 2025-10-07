add_executable(test_pow test_pow.cpp)
target_link_libraries(test_pow PRIVATE su2_lib)
add_test(NAME test_pow COMMAND test_pow)

add_executable(test_div test_div.cpp)
target_link_libraries(test_div PRIVATE su2_lib)
add_test(NAME test_div COMMAND test_div)

add_executable(test_div_zero test_div_zero.cpp)
target_link_libraries(test_div_zero PRIVATE su2_lib)
add_test(NAME test_div_zero COMMAND test_div_zero)

add_executable(test_dummy test.cpp)
target_link_libraries(test_dummy PRIVATE su2_lib)
add_test(NAME test_dummy COMMAND test_dummy)