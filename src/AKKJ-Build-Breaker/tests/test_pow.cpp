#include "su2.hpp"
#include <cstdint>
#include <vir/test.h>

TEST(test_pow_with_unit_matrix) {
  SU2_mat basis(1.0, 0.0, 0.0, 0.0);
  auto result = basis.pow(3);
  COMPARE(result, basis);
}

TEST(test_pow) {
  SU2_mat basis(0.5, 0.5, 0.5, 0.5);
  SU2_mat expected_result_pow_0(1.0, 0.0, 0.0, 0.0);
  SU2_mat expected_result_pow_1(0.5, 0.5, 0.5, 0.5);
  SU2_mat expected_result_pow_2(-0.5, 0.5, 0.5, 0.5);
  SU2_mat expected_result_pow_3(-1.0, 0.0, 0.0, 0.00);
  SU2_mat result = basis.pow(0);

  COMPARE(result, expected_result_pow_0);
  result = basis.pow(1);
  COMPARE(result, expected_result_pow_1);
  result = basis.pow(2);
  COMPARE(result, expected_result_pow_2);
  result = basis.pow(3);
  COMPARE(result, expected_result_pow_3);
}
