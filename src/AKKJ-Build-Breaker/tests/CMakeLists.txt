add_executable(test_pow test_pow.cpp ../src/su2.cpp)
add_test(NAME test_pow COMMAND test_pow)

add_executable(test_dummy test.cpp ../src/su2.cpp)
add_test(NAME test_dummy COMMAND test_dummy)