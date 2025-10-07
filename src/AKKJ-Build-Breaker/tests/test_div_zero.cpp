#include "su2.hpp"
#include <vir/test.h>
#include <stdexcept>

TEST_CATCH(test_div_zero, std::invalid_argument) {
  SU2_mat input_obj_0(1.0, 1.0, 1.0, 1.0);
  const double input_divisor_0{0.0};
  input_obj_0 /= input_divisor_0;
}
