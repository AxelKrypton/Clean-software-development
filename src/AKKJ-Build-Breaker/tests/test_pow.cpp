#include "su2.hpp"
#include <cstdint>
#include <vir/test.h>

TEST(test_pow) {
  SU2_mat base(1.0, 0.0, 0.0, 0.0);
  auto result = base.pow(3);
  COMPARE(result, base); // implicitly does memcmp
}
