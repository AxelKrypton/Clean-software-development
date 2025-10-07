#include "su2.hpp"
#include <vir/test.h>

TEST(test_div) {
  SU2_mat input_obj_0(1.0, 1.0, 1.0, 1.0);
  const double input_divisor_0{2.0};
  const SU2_mat expected_0(0.5, 0.5, 0.5, 0.5);
  input_obj_0 /= input_divisor_0;
  COMPARE(input_obj_0, expected_0);
}
